from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Item
from users.models import Profile
from django.urls import reverse_lazy
# from config.views import OwnerOnlyMixin


class ChallengeView(TemplateView):
    template_name = 'market.html'  # 마캣 화면

#-- 아이템 등록/삭제/수정
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
        즉, user_info에는 Profile 테이블에서 가져온 user_name이 저장되게 된다.
        이후, form_valid()메소드를 호출하면 db에 저장된 뒤 success_url로 redirect되게 된다.
        '''
        current_id = self.request.session.get('user')
        Profile_info = Profile.objects.get(id=current_id) # Profile에서 유저 정보를 가져오도록 한다.

        form.instance.user_info = Profile_info # form에 user_info 추가 (Profile 모델 참조해서)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs): 
        ''' 로그인이 되어 있지 않으면, 로그인 페이지로 이동하게끔 한다.'''
        current_user_id = request.session.get('user')  # 현재 접속 중인 user의 고유 id가 출력된다.
        
        if current_user_id is None: 
            return render(request, 'users/login.html', {'prev_path':request.path})

        return super().dispatch(request, *args, **kwargs)

class ItemUpdate(UpdateView):
    ''' 등록한 유저만 업데이트가 가능하도록 구현 - item_detail.html에서 설정'''
    model = Item
    fields = ['title', 'description', 'item_category'] # model에서 정의한 것을 form으로 가져온다.
    template_name = 'item_register.html' # render된 html 파일 정의
    success_url = reverse_lazy('market:market_page')  # 성공시 market페이지로 이동하도록 한다.

class ItemDelete(DeleteView):
    ''' 등록한 유저만 삭제가 가능하도록 구현 - item_detail.html에서 설정'''
    model = Item
    fields = ['title', 'description', 'item_category'] # model에서 정의한 것을 form으로 가져온다.
    template_name = 'item_delete_confirm.html' # render된 html 파일 정의
    success_url = reverse_lazy('market:market_page')  # 성공시 market페이지로 이동하도록 한다.


#-- 아이템 정보 및 디테일 정보 확인
class ItemView(ListView):
    '''
    ListView는 테이블로부터 객체 리스트를 가져와 출력한다.
    models.py파일에서 정의한 Item 테이블을 참조하도록 한다.
    ItemRegisterView에서 POST한 데이터들을 가져와서 html에서 출력하도록 한다.
    '''
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'item_index.html'
    context_object_name = 'items' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    paginate_by = 2 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정
    
    
class ItemDV(DetailView):
    '''
    등록된 아이템에 대한 상세 정보를 보여주도록 한다. -> Item model을 참조하도록 한다.
    DetailView는 html에서 객체의 context 값의 default가 object로 불러올 수 있게 된다.
    '''
    model = Item
    template_name = 'item_detail.html'

