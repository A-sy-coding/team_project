from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth.mixins import AccessMixin

def HomeView(request):
    id = request.session.get('user')#session데이터불러오기
    print(id)
    if id != None:
            user=Profile.objects.get(id=id)
            context={'user_name':user.user_name}
            return render(request,'home.html',context)
    if id == None:
            return render(request,'home.html')


# class OwnerOnlyMixin(AccessMixin):
#     '''
#     현재 접속중인 유저와 변경/삭제하고자 하는 글의 유저정보가 다르면, 접근을 제한하도록 한다. 
#     django 내장 함수인 AccessMixin클래스를 상속받아서 새로운 클래스를 재정의하도록 한다.
#     '''
#     raise_exception = True
#     permission_denied_messange = "Owner only can update/delete the object"

#     def dispatch(self, request, *args, **kwargs):
#         current_id = self.request.session.get('user')  # 현재 접속되어 있는 아이디 번호
#         obj = self.get_object() # 해당 form의 정보
#         # print('--------- 유저 정보 출력', obj.user_info_id)
#         if current_id != obj.user_info_id:
#             return self.handle_no_permission()
#         return super().dispatch(request, *args, **kwargs)