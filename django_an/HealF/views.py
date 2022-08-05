from django.shortcuts import render

from django.views.generic import TemplateView

#- TemplateView 이용 -> template 파일만을 렌더링하는 경우에 사용


# ------------------ main page ------------------------

class HealFMainView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        ctx = {}                             # 템플릿에 전달할 데이터
        return self.render_to_response(ctx)

class HealFchallengeView(TemplateView):
    template_name = 'challenge/challenge.html' # 챌린지 메인 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

class HealFexerciseView(TemplateView):
    template_name = 'exercise/exercise.html' # 운동 메인 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

class HealFcommunityView(TemplateView):
    template_name = 'community/commu.html' # 커뮤니티 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

class HealFmarketView(TemplateView):
    template_name = 'market/market.html' # 마켓 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

class HealFmypageView(TemplateView):
    template_name = 'mypage/mypage.html' # 나의정보 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)


# ------------------ login & sign-up page ------------------------

class HealFloginView(TemplateView):
    template_name = 'login/login.html' # login 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

class HealFsignupView(TemplateView):
    template_name = 'login/signup.html' # sign-up 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)


# ------------------ challenge page ------------------------

class Challenge_exerciseView(TemplateView):
    template_name = 'challenge/challenge_exercise.html' # challege화면의 운동하기 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

class Challenge_dietView(TemplateView):
    template_name = 'challenge/challenge_diet.html' #challenge화면의 다이어트하기 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)


# ------------------ market page ------------------------

class MkarketproductView(TemplateView):
    template_name = 'categorie/categorie.html' # market 화면의 제품 화면

    def get(self, request, *args, **kwargs):
        ctx = {}                             
        return self.render_to_response(ctx)

