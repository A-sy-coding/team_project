from django.shortcuts import render
import cv2
import threading

from django.views.decorators import gzip
from django.http import StreamingHttpResponse

# @gzip.gzip_page
# def OpenPoseView(request):
#     try:
#         cam = VideoCamera()
#         return StreamingHttpResponse(gen(cam), content_type = "multipart/x-mixed-replace;boundary=frame")
#     except:
#         pass
#     return render(request, 'ex.html')

# # caputre video 
# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         image = self.frame
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

#     def update(self):
#         while True:
#             (self.grabbed, self.frame) = self.video.read()

# def gen(camera):
#     while True:
#         frame = camera.get_frame()  # 인코딩한 뒤 바이트로 변환한 값 가져오기
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

import base64
def OpenPoseView(request):
    if (request.method == 'POST'):
        try:
            frame_ = request.POST.get('image')
            frame_ = str(frame_)
            data = frame_.replace('data:image/jpeg;base64,', '')    
            data = data.replace(' ', '+')
            imgdata = base64.b64decode(data)
            filename = 'some_image.jpg'
            
            with open(filename, 'wb') as f:
                f.write(imgdata)
        except:
            print('Error')
    
    return JsonResponse({'Json':data})
