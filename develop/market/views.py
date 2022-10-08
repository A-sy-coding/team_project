from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Item
from users.models import Profile
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
# from config.views import OwnerOnlyMixin


# import json
# from django.http import HttpResponse

from django.views.generic import FormView
from market.forms import SearchForm
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator

#-- 마켓 메인 페이지에서 아이템 정보 및 디테일 정보 확인 
class MarketView(ListView, FormView):
    '''
    ListView는 테이블로부터 객체 리스트를 가져와 출력한다.
    models.py파일에서 정의한 Item 테이블을 참조하도록 한다.
    ItemRegisterView에서 POST한 데이터들을 가져와서 html에서 출력하도록 한다.
    FormView를 추가로 상속받아 검색기능을 추가하도록 한다  -> Q사용 
    '''
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'market_home.html'
    context_object_name = 'items' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    paginate_by = 4 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정    
    
    form_class = SearchForm # 사용할 폼 설정

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word'] # form에서 정의한 필드 이름
        post_list = Item.objects.filter(
            Q(title__icontains=searchWord) | Q(description__icontains=searchWord) # 조건 설정
        )
        
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        # 페이징 기능도 추가
        page = self.request.GET.get('page', '1') #GET 방식으로 정보를 받아오는 데이터
        paginator = Paginator(Item.objects.all(), '10') #Paginator(분할될 객체, 페이지 당 담길 객체수)
        page_obj = paginator.page(page) #페이지 번호를 받아 해당 페이지를 리턴 get_page 권장
        context['page_obj'] = page_obj

        return render(self.request, 'search.html', context)
    
class MarketDV(DetailView):
    '''
    등록된 아이템에 대한 상세 정보를 보여주도록 한다. -> Item model을 참조하도록 한다.
    DetailView는 html에서 객체의 context 값의 default가 object로 불러올 수 있게 된다.
    '''
    model = Item
    template_name = 'item_detail.html'


#-- 아이템 등록/삭제/수정
class ItemRegisterView(CreateView):
    ''' 
    CreateView는 model과 form을 동시에 정의할 수 있다.
    market/item_register/ url에 연결되어 있고, name은 item_register으로 정의되어 있다.
    '''
    model = Item
    fields = ['title', 'description', 'item_category','img1','img2','img3','price','region'] # model에서 정의한 것을 form으로 가져온다.
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
    fields = ['title', 'description', 'item_category', 'img1', 'img2', 'img3','price','region'] # model에서 정의한 것을 form으로 가져온다.
    template_name = 'item_register.html' # render된 html 파일 정의
    success_url = reverse_lazy('market:market_page')  # 성공시 market페이지로 이동하도록 한다.

class ItemDelete(DeleteView):
    ''' 등록한 유저만 삭제가 가능하도록 구현 - item_detail.html에서 설정'''
    model = Item
    fields = ['title', 'description', 'item_category', 'img1', 'img2', 'img3','price','region'] # model에서 정의한 것을 form으로 가져온다.
    template_name = 'item_delete_confirm.html' # render된 html 파일 정의
    success_url = reverse_lazy('market:market_page')  # 성공시 market페이지로 이동하도록 한다.


#-- 각 카테고리별 물품 보여주기
class EquipmentView(ListView):
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'category_equipment.html'
    context_object_name = 'equipments' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    # paginate_by = 4 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정  

class ShoesView(ListView):
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'category_shoes.html'
    context_object_name = 'shoes' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    # paginate_by = 4 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정  

class SportswearView(ListView):
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'category_Sportwear.html'
    context_object_name = 'sportwears' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    # paginate_by = 4 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정  

class SupplementsView(ListView):
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'category_Supplements.html'
    context_object_name = 'supplements' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    # paginate_by = 4 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정  

class EtcView(ListView):
    model = Item  # models.py파일에서 Item 테이블 참조
    template_name = 'category_etc.html'
    context_object_name = 'etcs' # html로 넘어가는 객체 리스트의 변수명을 items로 설정
    # paginate_by = 4 # 한 페이지에 보여주는 객체 리스트의 숫자를 설정  

