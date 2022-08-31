from django.shortcuts import render
from django.views.generic import TemplateView

class ChallengeView(TemplateView):
    template_name = 'market.html'  # 마캣 화면

class ItemRegisterView(TemplateView):
    template_name = 'item_register.html'

class ItemView(TemplateView):
    template_name = 'test.html'