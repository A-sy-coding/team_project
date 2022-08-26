from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile

def HomeView(request):
    id = request.session.get('user')#session데이터불러오기
    print(id)
    if id != None:
            user=Profile.objects.get(id=id)
            context={'user_name':user.user_name}
            return render(request,'home.html',context)
    if id == None:
            return render(request,'home.html')