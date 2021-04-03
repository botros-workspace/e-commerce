from django.shortcuts import render
from .models import Item, Order
from django.views import generic

def checkout(request):
    return render(request, "checkout-page.html")

class HomeView(generic.ListView):
    model = Item
    template_name = "home-page.html"
    context_object_name = "items"

class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "product-detail.html"