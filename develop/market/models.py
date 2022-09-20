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
    modify_dt = models.DateTimeField('modify date', auto_now=True)

    class Meta:
        ordering = ('-modify_dt',) # modify_dt를 기준으로 내림차순으로 정렬한다.

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        '''
        개별 데이터 url을 가져온다.
        ItemDV를 참조하도록 한다. (name='item_detail')
        '''
        return reverse('market:item_detail', kwargs={'pk':self.id})
    
    def get_previous(self):
        return self.get_previous_by_modify_dt() # modify_dt를 기준으로 최신 데이터 반환
    
    def get_next(self):
        return self.get_next_by_modify_dy() # modify_dt를 기준으로 예전 데이터 반환