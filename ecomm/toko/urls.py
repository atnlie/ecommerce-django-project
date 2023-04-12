from django.urls import path
from . import views

app_name = 'toko'

urlpatterns = [
     path('', views.HomeListView.as_view(), name='home-produk-list'),
     path('product/<slug>/', views.ProductDetailView.as_view(), name='produk-detail'),
     path('checkout/', views.CheckoutView.as_view(), name='checkout'),
     path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
     path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
]
