from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def hello(request: HttpRequest) -> HttpResponse:
    return render(request, 'healf/index.html')