from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile
# Create your views here.
def main(request):
<<<<<<< Updated upstream
    return render(request,healf/main.html)
=======
        return render(request,'healf/main.html')

def mypage(request):
    return render(request,'healf/mypage.html')
>>>>>>> Stashed changes
