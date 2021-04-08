from django.urls import path, include 
from .views import HomeView, ItemDetailView, OrderSummaryView, add_to_cart, remove_from_cart, reduce_quantity_of_item

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name ='home-page'),
    path('product/<slug>/', ItemDetailView.as_view(), name ='product'),
    path('order-summary/', OrderSummaryView.as_view(), name ='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name ='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name ='remove-from-cart'),
    path('reduce-item-quantity/<slug>', reduce_quantity_of_item, name ='reduce-item-quantity'),
    
]
