from django.shortcuts import render

# Create your views here.


def exercise(request):
    return render(request, 'exercise.html')
