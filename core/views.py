from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem
from django.views import generic
from django.shortcuts import redirect
from django.utils import timezone

def checkout(request):
    return render(request, "checkout-page.html")

class HomeView(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"
    context_object_name = "items"

class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "product-detail.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_item, created = OrderItem.objects.get_or_create(item= item, user = request.user, ordered= False)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "Product quantity was updated")
        else:
            messages.info(request, "Item was added to your Cart")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your Cart")
    return redirect("core:product",slug= slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.quantity = 0
            order_item.save()
            messages.warning(request, "Item was removed from your Cart")
            return redirect("core:product",slug= slug)
        else:
            messages.warning(request, "Item is not in your Cart")
            return redirect("core:product", slug= slug)
    else:
        messages.warning(request, "No active order")
        return redirect("core:product",slug= slug)

    

