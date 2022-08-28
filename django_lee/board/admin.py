from django.contrib import admin
from .models import Board
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin) :
    summernote_fields = ('contents',) # summernote_fields에는 TextField중에서 summernote 위젯을 사용할 필드를 적어주면 됩니다
    list_display = (
        'title', 
        'contents', 
        'writer',
        'board_name',
        'hits', 
        'write_dttm', 
        'update_dttm'
    )
    list_display_links = list_display 