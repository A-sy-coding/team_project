from django.db import models
from users.models import Profile
class Board(models.Model) :
    title = models.CharField(max_length=64, verbose_name='글 제목')
    contents = models.TextField(verbose_name='글 내용')
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='작성자')
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')

    update_dttm = models.DateTimeField(auto_now=True, verbose_name='마지막 수정일')
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')

    def __str__(self) : 
        return self.title

    class Meta : 
        db_table = 'board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'