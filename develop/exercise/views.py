from django.shortcuts import render

# Create your views here.


def exercise(request):
    return render(request, 'exercise/exercise.html')

def arm(request):
    return render(request, 'exercise/arm.html')

def hache(request):
    return render(request, 'exercise/hache.html')
    
def shoulder(request):
    return render(request, 'exercise/shoulder.html')
    
def chest(request):
    return render(request, 'exercise/chest.html')

def exercisestart(request):
    return render(request, 'exercise/exercisestart.html')

def basic(request):
    return render(request,'exercise/basic.html')

def middle(request):
    return render(request,'exercise/middle.html')

def advanced(request):
    return render(request,'exercise/advanced.html') 