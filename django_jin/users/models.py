from django.db import models
from django.db import connection

class Profile(models.Model):
    id = models.AutoField(primary_key=True,verbose_name= 'id')
    user_id = models.CharField(max_length=32, unique=True, verbose_name='유저 아이디')
    user_pw = models.CharField(max_length=128, verbose_name='유저 비밀번호')
    user_name = models.CharField(max_length=16, verbose_name='유저 이름')
    user_email = models.EmailField(max_length=128, unique=True, verbose_name='유저 이메일')
    user_sex = models.CharField(max_length=16, verbose_name='유저 성별')
    user_birth = models.CharField(max_length=16,verbose_name='유저 생일')
    user_register_dttm = models.DateField(auto_now_add=True, verbose_name='계정 생성시간')
    def __str__(self):
        return self.user_id

    class Meta: # DB 테이블명 지정해주는 옵션
        db_table = 'profile' # 테이블명 지정
        verbose_name = '유저' # 해당 테이블의 닉네임
        verbose_name_plural = '유저' # 복수형 막아줌

class auth_number(models.Model):    
    auth_number = models.IntegerField(verbose_name='인증번호')