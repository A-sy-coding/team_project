from django.db import models
from django.urls import reverse
from users.models import Profile

item_choices = (
    ('1', '운동기구'),
    ('2', '운동화'),
    ('3', '운동복'),
    ('4', '보조식품'),
    ('5', '기타'),
)

class Item(models.Model):
    title = models.CharField('TITLE', max_length=30) # 등록물품 제목
    description = models.TextField('item description') # 물품 관련 설명
    item_category = models.CharField(max_length=20, choices = item_choices) # 물품 카테고리 종류
    user_info = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='로그인 유저', blank=True, null=True) # 로그인 된 유저 정보

    def __str__(self):
        return self.title