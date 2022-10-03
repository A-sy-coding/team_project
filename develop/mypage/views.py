from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import Profile
from market.models import Item
from community.models import Board
from challenge.models import Count_Post

def mypageView(request):
    current_id = request.session.get('user')
    if current_id is None: 
            return render(request, 'users/login.html', {'prev_path':request.path})
    Profile_info=Profile.objects.get(id=current_id)
    Item_info=Item.objects.filter(user_info=current_id)
    Board_info=Board.objects.filter(writer= current_id)
    Count_Post_info=Count_Post.objects.filter(user_info= current_id)
    context={'Profile_info':Profile_info,'Item_info':Item_info,'Board_info':Board_info,
        'Count_Post_info':Count_Post_info}

    return render(request, 'mypage.html', context)

# Create your views here.
# class mypageClass():#객체지향 따라해보기-모델들의 외래키 이름이 모두 다르기 때문에 폐기
#     def __init__(self, request):#mypageClass의 생성자. current_id를 변수로 갖는 인스턴스 생성  
#         self.current_id = request.session.get('user')
#     def get(self,model):#모델명을 선택하면 id가 일치하는 object들을 모두 획득한다.
#         try: 
#             self.get_object = model.objects.filter(id=Profile.self.current_id)
#         except:
#             self.get_object = None
#         return self.get_object

# def mypageView(request):
#     info=mypageClass(request) #mypageClass의 생성자 호출
#     if info.current_id is None: 
#             return render(request, 'users/login.html', {'prev_path':request.path})
#     Profile_info=info.get(Profile)#get함수를 재활용
#     Item_info=info.get(Item)
#     Board_info=info.get(Board)
#     Count_Post_info=info.get(Count_Post)
#     print(Item_info)
#     context={'Profile_info':Profile_info,'Item_info':Item_info,'Board_info':Board_info,
#         'Count_Post_info':Count_Post_info}

#     return render(request, 'mypage.html', context)
