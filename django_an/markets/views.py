from django.shortcuts import render

def market_main(request):

    return render(request, 'market.html')

def item_register(request):
    return render(request, 'item_register.html')