from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import Profile
from django.core.exceptions import ValidationError
from .models import auth_number
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
from random import randint


def login_view(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    elif request.method == "POST":
        user_id=request.POST['user_id']
        user_pw = request.POST['user_pw']
        user = authenticate(request,username=user_id, password=user_pw)

        if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('healf:main')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'users/logfail.html')




def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            Profile.objects.create_user(
                                        username=request.POST['user_id'],
                                        password=request.POST['password1'],
                                        name=request.POST['name'],
            )
            return redirect('/users/clear')
        return render(request, 'users/signup.html')
    return render(request, 'users/signup.html')

def clear(request):
    return render(request, 'users/clear.html')

def iddupl(request):
    if 'user_id' in request.POST:
        try:
            user = Profile.objects.get(username=request.POST['user_id'])
        except Exception as e:
            user=None
        if user==None:
            result = {
                'result':'success',
                'data' : "not exist"
            }
        else:
            result = {
                'result':'success',
                'data' : "exist"
            }
    return JsonResponse(result)


def email_validater(request): 

    if request.GET.get('email') is not None:        
        email=request.GET.get('email')   
        sendEmail = "jinus7949@naver.com"
        recvEmail = str(email)
        password = "wlsdntjr1!"
        smtpName = "smtp.naver.com"
        smtpPort = 587
        auth_num = randint(100000, 1000000)
        text = "인증번호는 "+str(auth_num)+"입니다"
        msg = MIMEText(text)
        msg['Subject']='HealF 이메일 인증'
        msg['From']=sendEmail
        msg['To']=recvEmail
        print(msg.as_string())
        s=smtplib.SMTP(smtpName, smtpPort)
        s.starttls()
        s.login(sendEmail, password)
        s.sendmail(sendEmail, recvEmail, msg.as_string())
        s.close
        auth_number.objects.create(auth_number = auth_num)
        result = {
                'result':'success',
                'auth_info' : str(auth_num)
            }
        return JsonResponse(result)
    else:
        raise ValidationError("오류입니다")


def auth_num_validater(request):
    if request.POST['auth_num'] == auth_number.objects.get(auth_number[0]):
        result = {
                'result':'success',
                'data' : "cor"
            }
        auth_number.objects.all().truncate()
        return JsonResponse(result)

    else:
        result = {
                'result':'success',
                'data' : "no cor"
            }
        auth_number.objects.all().truncate()
        return JsonResponse(result) 


# Create your views here.
