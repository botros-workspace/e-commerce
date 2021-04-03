from django.urls import path, include 
from .views import HomeView, ItemDetailView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name ='home-page'),
    path('product/<slug>/', ItemDetailView.as_view(), name ='product'),
]
