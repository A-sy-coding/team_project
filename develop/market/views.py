from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Item
from django.urls import reverse_lazy

class ChallengeView(TemplateView):
    template_name = 'market.html'  # 마캣 화면

class ItemRegisterView(CreateView):
    ''' 
    CreateView는 model과 form을 동시에 정의할 수 있다.
    market/item_register/ url에 연결되어 있고, name은 item_register으로 정의되어 있다.
    '''
    model = Item
    fields = ['title', 'description', 'item_category'] # model에서 정의한 것을 form으로 가져온다.
    template_name = 'item_register.html' # render된 html 파일 정의
    success_url = reverse_lazy('market:market_page')  # 성공시 market페이지로 이동하도록 한다.

    def form_valid(self, form):
        '''
        form에 연결된 모델 객체의 user_info 필드에는 현재 로그인된 사용자의 user 객체 정보를 할당한다.
        이후, form_valid()메소드를 호출하면 db에 저장된 뒤 success_url로 redirect되게 된다.
        '''
        form.instance.user_info = self.request.session.get('user') # 현재 접속 중인 user의 고유 id가 출력된다.
        return super().form_valid(form)

class ItemView(TemplateView):
    template_name = 'test.html'