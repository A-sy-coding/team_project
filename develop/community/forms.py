from django import forms
from .models import Board
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class BoardWriteForm(forms.ModelForm) : 
    title=forms.CharField(
        label = '글제목',
        widget = forms.TextInput(
            attrs={
                'placeholder' : '게시글 제목',
                'input[type="text"]' : {'width' : '80%', 'height' : '30px'}
            }),
        required=True,
    )

    contents = SummernoteTextField()

    field_order = [
        'title',
        'contents'
    ]

    class Meta : 
        model = Board
        fields = [
            'title',
            'contents',
        ]
        widgets = {
            'contents' : SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px', 'resize': 'vertical'}})
        }

    def clean(self):
        cleand_data = super().clean()

        title = cleand_data.get('title', '')
        contents = cleand_data.get('contents', '')

        if title == '' :
            self.add_error('title', '글 제목을 입력하세요.')
        elif contents == '':
            self.add_error('contents', '글 내용을 입력하세요')
        else : 
            self.title = title
            self.contents = contents