from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
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
        return render(request,'users/signup.html')
# Create your views here.