from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
def login_view(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    elif request.method == "POST":
        user_id=request.POST['user_id']
        user_pw = request.POST['user_pw']
        user = authenticate(request,username=user_id, password=user_pw)

        if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('healf:main')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'users/logfail.html')
        

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            Profile.objects.create_user(
                                        username=request.POST['user_id'],
                                        password=request.POST['password1'],
                                        name=request.POST['name'],
            )
            return redirect('/users/clear')
        return render(request, 'users/signup.html')
    return render(request, 'users/signup.html')

def clear(request):
    return render(request, 'users/clear.html')
# Create your views here.