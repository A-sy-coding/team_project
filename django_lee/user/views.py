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
            return redirect('/')

        else : 
            context['forms'] = loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'user/login.html', context)