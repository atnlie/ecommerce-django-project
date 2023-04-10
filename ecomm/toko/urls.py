from django.urls import path
from . import views

app_name = 'toko'

urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),
     path('product/', views.ProductDetailView.as_view(), name='product_detail'),
     path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
