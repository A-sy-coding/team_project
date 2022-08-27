from django.db import models
from users.models import Profile

class Count_Post(models.Model):
    user_count = models.CharField(max_length=10, null=True, verbose_name='스쿼트 개수')
    user_info = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='로그인 유저', blank=True, null=True)
    user_dt = models.DateField(auto_now_add=True, verbose_name='스쿼트 챌린지 시작시간', null=True)
    user_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.user_count

    class Meta:
        ordering = ('-user_dt',) # user_dt를 기준으로 내림차순
    
