from django.shortcuts import render
from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class ProductDetailView(generic.TemplateView):
    template_name = 'product_detail.html'

class CheckoutView(generic.TemplateView):
    template_name = 'checkout.html'