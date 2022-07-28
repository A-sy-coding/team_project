from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
def login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('healf/main.html'))
        else:
            # Return an 'invalid login' error message.
            return render(request, 'healf/main.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            auth.login(request, user)
            return redirect('/users/clear')
        return render(request, 'users/signup.html')
    return render(request, 'users/signup.html')

def clear(request):
    return render(request, 'users/clear.html')
# Create your views here.