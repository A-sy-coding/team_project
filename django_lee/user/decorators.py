import re
from django.shortcuts import redirect
from .models import User

def login_required(func):
    def wrapper (request, *args, ** kwargs):
        login_session = request.session.get('login_session', '')

        if login_session == '':
            return redirect('/user/login') # 로그아웃 상태이면 로그인 페이지로

        return func(request, *args, ** kwargs)  # 로그인이면
    
    return wrapper