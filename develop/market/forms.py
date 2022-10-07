from django import forms

#-- sesarch용 form 생성
class SearchForm(forms.Form):
    search_word = forms.CharField(label='검색어를 입력하세요.')