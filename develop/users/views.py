from django.shortcuts import render,redirect
from .models import Profile
from django.core.exceptions import ValidationError
from .models import auth_number
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
from random import randint
from config.settings import get_secret

#로그인 함수
def login_view(request):

    if request.method == "GET":
        prev_path = request.GET.get('prev_path') # a href으로 이전 페이지 url을 받아오도록 한다.
        return render(request, 'users/login.html', {'prev_path':prev_path})

    elif request.method == "POST":
        login_user_id=request.POST['user_id']
        login_user_pw = request.POST['user_pw']
        
        prev_path = request.POST.get('prev_path') # login 페이지에서 로그인을 누르면 POST방식으로 데이터 전송
                                                  # 이전 경로를 기억하도록 하여 prev_path로 저장
        print('이전 경로 --------------')
        print(prev_path)
    
    try:
        myuser = Profile.objects.get(user_id__exact=login_user_id,user_pw__exact=login_user_pw)    
        print(myuser.id)
    except:
        myuser = None    
    
    if myuser != None:
        request.session['user'] = myuser.id
        # Redirect to a success page.
        return redirect(prev_path)
        
    else:
        contents = {'fail':'로그인에 실패하였습니다.' , 'prev_path':prev_path}
            # Return an 'invalid login' error message.
        return render(request,'users/login.html',contents)




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
        except:
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
        password=get_secret('EMAIL_HOST_PASSWORD')
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
        result = {
                'result':'success',
                'auth_info' : str(auth_num)
            }
        s.close
        auth_number.objects.create(auth_number = auth_num)
        return JsonResponse(result)
    else:
        raise ValidationError("오류입니다")


def auth_num_validater(request):#인증번호
    if 'auth_num' in request.POST:
        try:
            my_auth_number=auth_number.objects.get(auth_number=request.POST['auth_num'])
        except Exception:
            my_auth_number=None
            result = {
                    'result':'success',
                    'data' : "no cor"
                }
            auth_number.objects.all().delete()
            return JsonResponse(result)
        result = {
                'result':'success',
                'data' : "cor"
            }
        auth_number.objects.all().delete()
        return JsonResponse(result)



# Create your views here.
def logout(request):
    request.session.pop('user')
    return redirect('home')