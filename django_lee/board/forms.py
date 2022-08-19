from django import forms
from .models import Board
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class BoardWriteForm(forms.ModelForm) : 
    title=forms.CharField(
        label = '글 제목',
        widget = forms.TextInput(
            attrs={
                'placeholder' : '게시글 제목'
        }),
        required=True,
    )

    contents = SummernoteTextField()

    options = ( #Select위젯의 옵션을 설정
        ('python', '파이썬 게시판'), # 'Python'은 Model에 저장
        ('JavaScript', '자바스크립트 게시판') # '자바스크립트 게시판'은 화면에 렌더링
    )

    board_name=forms.CharField(
        label = '게시판 선택',
        widget = forms.Select(),
        choices = options
    )

    field_order = [
        'title',
        'board_name',
        'contents'
    ]

    class Meta : 
        model = Board
        fields = [
            'title',
            'contents',
            'board_name'
        ]
        widget = {
            'contents' : SummernoteWidget()
        }

    def clean(self):
            cleand_data = super().clean()

            title = cleand_data.get('title', '')
            contents = cleand_data.get('contents', '')
            board_name = cleand_data.get('board_name', 'Python')

            if title == '' :
                self.add_error('title', '글 제목을 입력하세요.')
            elif contents == '':
                self.add_error('contents', '글 내용을 입력하세요')
            else : 
                self.title = title
                self.contents = contents
                self.board_name = board_name