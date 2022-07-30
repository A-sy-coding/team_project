from django.shortcuts import render
import cv2
import threading

from django.views.decorators import gzip
from django.http import StreamingHttpResponse


# import base64
# def OpenPoseView(request):
#     if (request.method == 'POST'):
#         try:
#             frame_ = request.POST.get('image')
#             frame_ = str(frame_)
#             data = frame_.replace('data:image/jpeg;base64,', '')    
#             data = data.replace(' ', '+')
#             imgdata = base64.b64decode(data)
#             filename = 'some_image.jpg'
            
#             with open(filename, 'wb') as f:
#                 f.write(imgdata)
#         except:
#             print('Error')
    
#     return JsonResponse({'Json':data})

# open-pose 실행 클래스
# class CapturePose()

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
import socketio
from django.http import JsonResponse




def HtmlWebcamView(request):

    # return render(request, 'webcam.html')
    return render(request, 'ex.html')
    
    
def canvas_image(request):
    if (request.method == 'POST'):
        try:
            frame = request.POST.get('imageBase64')
            print(frame)

            text = 'abcdddddd'
            # frame_ = str(frame_)
            # data = frame_.replace('data:image/jpeg;base64,', '')    
            # data = data.replace(' ', '+')
            # imgdata = base64.b64decode(data)
            # filename = 'some_image.jpg'
            
            # with open(filename, 'wb') as f:
            #     f.write(imgdata)
        except:
            print('Error')
    return text
    # return JsonResponse({'Json':frame})

