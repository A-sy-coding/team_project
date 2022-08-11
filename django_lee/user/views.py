from http.client import REQUEST_ENTITY_TOO_LARGE
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import User
from argon2 import PasswordHasher
from .forms import RegisterForm, LoginForm
# Create your views here.

def register(request : HttpRequest) -> HttpResponse:
    register_form = RegisterForm()
    context = {'forms': register_form}

    if request.method == 'GET' : 
        return render(request, 'user/register.html', context)
    
    elif request.method == 'POST' :
        register_form = RegisterForm(request.POST)
        if register_form.is_valid() : # form.py의 clean 호출
            user=User(
                user_id = register_form.user_id,
                user_pw = register_form.user_pw,
                user_name = register_form.user_name,
                user_email = register_form.user_email
            )
            user.save()
            return redirect('/')
        else : 
            context['forms'] = register_form
            if register_form.errors : 
                for value in register_form.errors.values() :
                    context['error'] = value
        return render(request, 'user/register.html', context)

def login(request : HttpRequest) -> HttpResponse:
    loginform = LoginForm()
    context={'forms': loginform}

    if request.method=='GET':
        return render(request, 'user/login.html', context)

    elif request.method=='POST':
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            request.session['login_session'] = loginform.login_session
            request.session.set_expiry(0) #set_expiry메서드는 세션만료시간을 설정합니다. 0을 넣을 경우 브라우저를 닫을 시 세션 쿠키 삭제 + DB의 만료기간은 14일로 설정됩니다.
            return redirect('/')

        else : 
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')