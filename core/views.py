from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem, BillingAddress
from django.views import generic
from .forms import CheckOutForm
from django.shortcuts import redirect
from django.utils import timezone

class CheckoutView(generic.View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            'form':form
        }
        return render(self.request, "checkout-page.html",context=context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            if form.is_valid():
                street_name = form.cleaned_data.get('street_name')
                building_number = form.cleaned_data.get('building_number')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_shipping_address = form.cleaned_data.get('same_shipping_address')
                save_information = form.cleaned_data.get('save_information')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_name = street_name,
                    building_number= building_number,
                    country= country,
                    zip= zip
                ) 
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect("core:check-out")
            messages.warning(self.request, "Checkout Failed")
            return redirect("core:check-out")
        except ObjectDoesNotExist:
            messages.error(self.request, "You ddon't have an active order")
            return redirect("core:home-page")

            
            messages.warning(self.request,"check")
            return redirect("core:check-out")

class HomeView(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"
    context_object_name = "items"

class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "product-detail.html"

class OrderSummaryView(LoginRequiredMixin, generic.View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            context = {                                 
                'object':order
            }   
            return render(self.request, 'order-summary.html',context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You ddon't have an active order")
            return redirect("/")

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_item, created = OrderItem.objects.get_or_create(item= item, user = request.user, ordered= False)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
        else:
            messages.info(request, "Item was added to your Cart")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item was added to your Cart")
    return redirect("core:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.warning(request, "Item was removed from your Cart")
            return redirect("core:order-summary")
        else:
            messages.warning(request, "Item is not in your Cart")
            return redirect("core:order-summary")
    else:
        messages.warning(request, "No active order")
        return redirect("core:order-summary")

@login_required
def reduce_quantity_of_item(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user = request.user, ordered=False)[0]
            if order_item.quantity -1 == 0:
                order.items.remove(order_item)
            else:
                order_item.quantity -= 1
                order_item.save()
            return redirect("core:order-summary")
        else:
            messages.warning(request, "Item is not in your Cart")
            return redirect("core:order-summary")
    else:
        messages.warning(request, "No active order")
        return redirect("core:order-summary")


