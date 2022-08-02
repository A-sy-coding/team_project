from django.shortcuts import render
import cv2
import threading

from django.views.decorators import gzip
from django.http import StreamingHttpResponse


# 영상 클래스
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)  # 카메라 열기
        (self.grabbed, self.frame) = self.video.read() # 카메라 읽기
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):  # 카메라 종료
        self.video.release()

    def get_frame(self):  # 프레임 캡처
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)  # image를 Binary형태로 읽는다.
        return jpeg.tobytes()
    
    def update(self):  # 프레임 캡처 계속 반복
        while True:
            (self.grabbed, self.frame) = self.video.read()

    
def gen(camera):
    while True:
        frame = camera.get_frame()
        # yeild는 제너레이터를 반환하게 된다.
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@gzip.gzip_page
def OpenPoseView(request):
    try:
        cam = VideoCamera()
        response = StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame") 
        print('----- response -------')
        print(response)
        return response
    except:
        print('Camera가 존재하지 않습니다.')


####################################
# html로 webcam 가져오는 방법 구현
###################################
import base64
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import numpy as np

# 필요한 model 패키지
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
    # return render(request, 'ex.html')
    return render(request, 'ex2.html')



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

