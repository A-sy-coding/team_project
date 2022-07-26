from django.shortcuts import render

from django.views.generic import TemplateView

#- TemplateView 이용 -> template 파일만을 렌더링하는 경우에 사용
class HealFModelView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request, *args, **kwargs):
        ctx = {}                             # 템플릿에 전달할 데이터
        return self.render_to_response(ctx)
