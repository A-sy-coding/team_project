from django.db import models
from users.models import Profile

# POST를 통해 얻은 데이를 이용해 squat count를 세고, 데이터베이스에 저장하도록 한다.
# class Count_Post(models.Model):
#     title = models.CharField(max_length=50)
#     text = models.TextField()

#     def __str__(self):
#         return self.text

class Count_Post(models.Model):
    user_count = models.CharField(max_length=10, null=True, verbose_name='스쿼트 개수')
    user_info = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='로그인 유저', blank=True, null=True)
    user_dt = models.DateField(auto_now_add=True, verbose_name='스쿼트 챌린지 시작시간', null=True)

    def __str__(self):
        return self.user_count
    
