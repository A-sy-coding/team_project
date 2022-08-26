from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt
import numpy as np
import os
from pathlib import Path

# db에 count값 저장시 필요 패키지
from .models import Count_Post
from users.models import Profile
from django.http import HttpResponse

# 필요한 ai model 패키지
import torch, cv2
from challenge.utils import OpenPoseNet
from challenge.webcam import img_preprocess, get_pafs_heatmaps, pose_test, findAngle, delete_duplicate, squat_condition


#--- TemplateView
class ChallengeView(TemplateView):
    template_name = 'challenge/challenge.html' # 챌린지 화면
    

class Challenge_exerciseView(TemplateView):
    '''
    Description :
        로그인이 되면 바로 접속이 가능하도록 하고, 로그인이 안되어 있으면 로그인 화면으로 redirect되도록 한다.
    '''
    template_name = 'challenge/challenge_exercise.html' # challege화면의 운동하기 화면

    def dispatch(self, request, *args, **kwargs): 
        login_session = request.session.get('user')
        
        if login_session is None:
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)


class Challenge_dietView(TemplateView):
    template_name = 'challenge/challenge_diet.html' #challenge화면의 다이어트하기 화면

#--- AI model
def setting_model():
    '''
    학습시킨 모델(pth)파일을 가져와 OpenPoseNet 신경망에 넣기
    '''
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    weights = '../../pose_model_scratch.pth'

    # 모델 정의 
    net = OpenPoseNet()

    if device == 'cuda:0':
        net_weights = torch.load(weights)
    else:
        net_weights = torch.load(weights, map_location=device)

    keys = list(net_weights.keys())
    weights_load = {}

    # 로드한 내용을 이 책에서 구축한 모델의
    # 파라미터명 net.state_dict().keys()로 복사
    for i in range(len(keys)):
        weights_load[list(net.state_dict().keys())[i]] = net_weights[list(keys)[i]]

    # 복사한 내용을 모델에 할당
    state = net.state_dict()
    state.update(weights_load)
    net.load_state_dict(state)

    return net

def setting_squat(img, net):
    '''
    squat 카운트 세는 세팅 설정 
    params:
        img(np.naddray) -> 이미지를 배열로 변경시킨 값을 가진다.
        net(OpenPoseNet) -> 학습시킨 가중치를 적용시킨 OpenPoseNet 모델이다.
    '''
    # 이미지 전처리
    preprocess_img = img_preprocess(img)
    # pafs, heatmaps 구하기
    pafs, heatmaps = get_pafs_heatmaps(net, preprocess_img, img)
    # pose test 해보기 --> 관절 위치 
    out, joint_lmList = pose_test(img, pafs, heatmaps)

    # joint_lmList 전처리 --> 중복된 값 없게 설정
    joint_dict = delete_duplicate(joint_lmList)

    return joint_dict, out
        

def HtmlWebcamView(request):
    '''
    챌린지 페이지에서 start를 누르면 넘어가도록 하는 페이지 
    squat_record.html과 render된다.
    suqat_record.html에서는 javascript를 이용하여 webcam을 키고, 데이터를 전송하도록 해준다.
    데이터는 'webcam/record_video'으로 전송되게 된다. (record.js에서 설정)
    '''
    # return render(request, 'webcam.html') 
    return render(request, 'challenge/squat_record.html')



@csrf_exempt
def record_video(request):
    '''
    squat_reocrd.html에서 webcam을 녹화하고 해당 영상을 'webcam/record_video'으로 전송하게 된다.
    따라서, form형태의 데이터를 request로 받게 된다.
    POST로 받은 데이터를 데이터 처리를 통해 프레임단위 이미지로 나누어 결과값을 도출한다.
    models.py에서 db를 저장할 폼을 만들고 해당 폼 안에 스쿼트 count 값을 넣게 된다.
    이후, 처리가 완료된 메세지를 'webcam/record_video'로 HttpResponse하게 한다.
    response값은 record.js파일에서 ajax가 data로 받아 h2태그의 반환값으로 출력되게 한다. (비동기 방식으로)
    '''
    # POST 받기 전에 한번만 실행하도록 설정
    net = setting_model() # 학습시킨 openpose 모델 --> 한번만 실행하도록 밖에다 빼서 실행
    print('-------- 모델 세팅 완료 --------------')
    
    # 현재 로그인 정보 가져오기
    current_user_id = request.session.get('user')  # 현재 접속 중인 user의 고유 id가 출력된다.
    user_info = Profile.objects.get(id=current_user_id) # Profile에서 유저 정보를 가져오도록 한다.
    
    if (request.method == 'POST'):

        video_data = request.FILES['video'].read()
        # print(video_data)
        # print(type(video_data)) # bytes 타입

        # 임시로 mp4로 저장
        Base_path = Path(__file__).resolve().parent
        File_output = os.path.join(Base_path,"webcam.mp4")

        # writing binary(bytes 영상을 mp4로 변환하여 저장)
        with open(File_output, "wb") as out_file:
            out_file.write(video_data)

        # 비디오를 프레임단위로 끊기
        capture = cv2.VideoCapture(File_output)
        success, _ = capture.read()
        index = 0

        count = 0
        direction = 0
        form = 0
        feedback = "Fix Form"
        while success:
            success, img = capture.read()  # 배열 이미지 가져오기

            if success == False:
                break
            else:
                joint_dict, out = setting_squat(img, net) # joint_dict 반환( 중복제거된 관절 정보들 -> 관절 번호 및 해당 , x,y좌표 )

                # 스쿼트 시작 
                count, form, direction, feedback, out = squat_condition(joint_dict, count, form, direction, feedback, out)
                # print(joint_dict)
                index += 1
                print(f'--------- {index}번째 이미지... --------- ')
                # print(count, form, feedback)
                # cv2.imwrite('tem_img/img_{}_sample.png'.format(index), out)

        print('--------- 최종 Squat count -------------')
        print(int(count))

        # webcam.mp4 파일 삭제
        try:
            if os.path.isfile(File_output):
                os.remove(File_output)
        except:
            pass

        # Count_Post 모델 객체 생성
        string_count = str(int(count))
        temp = Count_Post(user_count=string_count, user_info=user_info)
        temp.save()
        # Count_Post.objects.create(user_count = string_count)
        
        # post = Count_Post(user_count=string_count)
        # post.save()

        print('----------DB 조회 ---------------')
        print(Count_Post.objects.all().values())

        success = 'You complete ' + string_count + ' squat challenge!'
        return HttpResponse(success)