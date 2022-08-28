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

    options = (
        ('Python', '파이썬 게시판'),
        ('JavaScript', '자바스크립트')
    )

    board_name = forms.ChoiceField(
        label = '게시판 선택',
        widget = forms.Select(),
        choices=options
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
        widgets = {
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