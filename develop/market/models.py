from django.db import models
from django.urls import reverse
from users.models import Profile

#-- 썸네일용 라이브러리
from imagekit.models import ImageSpecField 
from imagekit.processors import ResizeToFill 

item_choices = (
    ('운동기구', '운동기구'),
    ('운동화', '운동화'),
    ('운동복', '운동복'),
    ('보조식품', '보조식품'),
    ('기타', '기타'),
)

region_choices = (
    ('동구', '동구'),
    ('서구', '서구'),
    ('남구', '남구'),
    ('북구', '북구'),
    ('광산구', '광산구'),
)

####### Inline을 사용하여 Item과 Upload_file이 같이 적용되도록 한다.
# 아이템 하나당 여러개의 이미지들이 등록 가능함. -> 1 : N관계 -> ForeignKey 사용 가능해보인다.
# Upload_img를 정의하여 이미지 리스트를 받아와 Upload_img model에 1:N 관계로 저장되게 한다.
# class Upload_file(models.Model):
#     image = models.FileField(upload_to='market_item/%Y/%m/%d/', null=False, default=None)


class Item(models.Model):
    title = models.CharField('물품 제목', max_length=30) # 등록물품 제목
    description = models.TextField('물품 설명') # 물품 관련 설명
    item_category = models.CharField('물품 종류',max_length=20, choices = item_choices) # 물품 카테고리 종류
    user_info = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='로그인 유저', blank=True, null=True) # 로그인 된 유저 정보
    price = models.DecimalField(max_digits=10, decimal_places=0) # 물품 가격
    region = models.CharField('위치', max_length=5, choices=region_choices, null=False)
    modify_dt = models.DateTimeField('modify date', auto_now=True)

    ######### 멀티 이미지 추가 코드 (3개로 제한되게끔 구현한다.)
    img1 = models.FileField('물품 이미지',upload_to='market_item/%Y/%m/%d/', null=False, default=None)
    img2 = models.FileField(upload_to='market_item/%Y/%m/%d/', null=False, default=None)
    img3 = models.FileField(upload_to='market_item/%Y/%m/%d/', null=False, default=None)
    img_thumbnail = ImageSpecField(source = 'img1', processors = [ResizeToFill(240, 240)]) # 썸네일 지정

    #--  좋아요 기능
    # liked_users = models.ManyToManyField('users.Profile', related_name='liked_posts')

    class Meta:
        ordering = ('-modify_dt',) # modify_dt를 기준으로 내림차순으로 정렬한다.

    def __str__(self):
        return self.title
    
    def count_likes_user(self): # total likes_user
        return self.likes_user.count()
        
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


# class Like(models.Model):
#     user = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
#     post = models.ForeignKey('Item', on_delete=models.CASCADE)