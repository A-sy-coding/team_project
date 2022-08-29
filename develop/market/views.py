from django.shortcuts import render
from django.views.generic import TemplateView

class ChallengeView(TemplateView):
    template_name = 'market.html'  # 마캣 화면

