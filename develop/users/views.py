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
        login_user_id=request.POST['user_id']
        login_user_pw = request.POST['user_pw']
        try:
            myuser = Profile.objects.get(user_id=login_user_id)
        except Profile.DoesNotExist:
            myuser = None
        if myuser is not None:
            if login_user_pw == myuser.user_pw:
                request.session['user'] = myuser.id

                # Redirect to a success page.
                return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'users/logfail.html')




def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    if request.method == 'POST':
        user_birth=request.POST['birthyy']+'-'+request.POST['birthmm']+'-'+request.POST['birthdd']
        Profile.objects.create(
            user_id=request.POST['user_id'], 
            user_pw=request.POST['password1'],
            user_email=request.POST['user_email'],
            user_name=request.POST['user_name'],
            user_sex=request.POST['user_sex'],
            user_birth=user_birth
        )
        return redirect('/users/clear')
    return render(request, 'users/register.html')

def clear(request):#가입성공 시 호출할 창
    return render(request, 'users/clear.html')

def iddupl(request):#아이디 유효성 검사기
    if 'user_id' in request.POST:    
        try:
            user_id = Profile.objects.get(user_id=request.POST['user_id'])
        except Exception as e:
            user_id=None
        if user_id==None:
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


def email_validater(request): #이메일 인증기
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


def auth_num_validater(request):#인증번호
    if 'auth_num' in request.POST:
        try:
            my_auth_number=auth_number.objects.get(auth_number=request.POST['auth_num'])
        except Exception as e:
            my_auth_number=None
            result = {
                    'result':'success',
                    'data' : "no cor"
                }
            return JsonResponse(result)
        result = {
                'result':'success',
                'data' : "cor"
            }
        return JsonResponse(result)



# Create your views here.
def logout(request):
    request.session.pop('user')
    return redirect('healf:main')