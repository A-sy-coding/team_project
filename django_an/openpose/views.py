from django.shortcuts import render, redirect


####################################
# html로 webcam 가져오는 방법 구현
###################################
import cv2
import base64
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import numpy as np
import os

# db에 count값 저장시 필요 패키지
from .models import Count_Post
from django.http import HttpResponse

# 필요한 ai model 패키지
import torch
from openpose.utils import OpenPoseNet
from openpose.webcam import img_preprocess, get_pafs_heatmaps, pose_test, findAngle, delete_duplicate, squat_condition

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

    # return render(request, 'webcam.html') 
    return render(request, 'squat_record.html')



@csrf_exempt
def record_video(request):
    # POST 받기 전에 한번만 실행하도록 설정
    net = setting_model() # 학습시킨 openpose 모델 --> 한번만 실행하도록 밖에다 빼서 실행
    print('-------- 모델 세팅 완료 --------------')
    
    if (request.method == 'POST'):

        video_data = request.FILES['video'].read()
        # print(video_data)
        # print(type(video_data)) # bytes 타입

        # 임시로 mp4로 저장
        File_output = "webcam.mp4"

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
        if os.path.isfile(File_output):
            os.remove(File_output)

        # Count_Post 모델 객체 생성
        string_count = str(int(count))
        post = Count_Post(text=string_count)
        post.save()

        # print('----------DB 조회 ---------------')
        # print(Count_Post.objects.all().values())

        success = 'You complete ' + string_count + ' squat challenge!'
        return HttpResponse(success)                                                                                                                                                                                                                                                     
    

@csrf_exempt
def canvas_image(request):

    count = 0
    direction = 0
    form = 0
    feedback = "Fix Form"
    net = setting_model() # 학습시킨 openpose 모델 --> 한번만 실행하도록 밖에다 빼서 실행
    
    if (request.method == 'POST'):
        try:
            index = request.POST.get('index')
            frame = request.POST.get('imageBase64')

            header, data = frame.split(';base64,') # header은 이미지 타입, data에는 base64로 인코딩된 이미지
            data_format, ext = header.split('/') # ext는 파일 확장자(png)

            image_data = base64.b64decode(str(data))  # base64 이미지 디코드
            data_np = np.fromstring(image_data, dtype='uint8')
            img = cv2.imdecode(data_np, 1)
            
            joint_dict, out = setting_squat(img, net) # joint_dict 반환( 중복제거된 관절 정보들 )

            # 스쿼트 시작 ( 스쿼트 시작 기준성립하면 count를 세도록 한다. )
            print(f'--------- 현재 {index} 번째 index')
            count, form, direction, feedback, out = squat_condition(joint_dict, count, form, direction, feedback, out)
            print(joint_dict)
            print(count, form, feedback)
            cv2.imwrite('img_{}_sample.png'.format(index), out)
            # squat(net)            

        except:
            pass
    return JsonResponse(frame, safe=False)

