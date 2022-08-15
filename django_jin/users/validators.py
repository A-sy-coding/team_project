import string
from django.core.exceptions import ValidationError
# from users.models import Profile
from random import randint


class email_val:
    def __init__(self, auth_number = None):
        self.auth_number = auth_number
    def new_auth_number(self):
         temp_number = randint(100000, 1000000)
         self.auth_number = temp_number 

         return self.auth_number
    def reset(self):
        self.auth_number = None 

    def email_validater(request): 

        if request.GET.get('email') is not None:        
            email=request.GET.get('email')   
            sendEmail = "jinus7949@naver.com"
            recvEmail = str(email)
            password = "wlsdntjr1!"
            smtpName = "smtp.naver.com"
            smtpPort = 587

            random_func = email_val()
            auth_number= random_func.new_auth_number() 
            print('----------- auth number -----------')
            print(auth_number)
            text = "인증번호는 "+str(auth_number)+"입니다"
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
            result = {
                    'result':'success',
                    'auth_info' : str(auth_number)
                }
            return JsonResponse(result)
        else:
            raise ValidationError("오류입니다")


    def auth_num_validater(request):
        if request.POST['auth_num'] == email_val.auth_number:
            result = {
                    'result':'success',
                    'data' : "cor"
                }
            return JsonResponse(result)

        else:
            raise ValidationError("잘못된 인증번호입니다.")        



