from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from user.models import User


def hello(request: HttpRequest) -> HttpResponse:
    context = {}

    # 클라이언트가 로그인 세션정보를 가지고있는지 체크
    login_session = request.session.get('login_session', '')

    if login_session == '':
        context['login_session'] = False # 로그인 정보 없으면
    else:
        context['login_session'] = True # 로그인 정보 있으면

    return render(request, 'healf/index.html', context)