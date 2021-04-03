from django.urls import path, include 
from .views import home_page, item_detail

app_name = 'core'

urlpatterns = [
    path('', home_page, name ='home-page'),
    path('product/', item_detail, name ='item-detail'),
]
