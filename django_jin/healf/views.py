from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile
# Create your views here.
def main(request):
        user_id = request.session.get('user')#session데이터불러오기
        myuser_info = Profile.objects.get(pk=user_id)
        return render(request,'healf/main.html',content={'user_id':myuser_info})

def mypage(request):
    return render(request,'healf/mypage.html')