from django.shortcuts import render
from .models import Item, Order

def home_page(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context=context)

def item_detail(request):
    context = {
        'item':Item.objects.all() 
    }
    return render(request, "product-page.html", context=context)

def checkout(request):
    context = {
        'order':Order.objects.all()
    }
    return render(request, "checkout-page.html", context=context)