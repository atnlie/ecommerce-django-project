from django.views import generic

from .models import ProdukItem

class HomeListView(generic.ListView):
    template_name = 'home.html'
    queryset = ProdukItem.objects.all()

class ProductDetailView(generic.TemplateView):
    template_name = 'product_detail.html'

class CheckoutView(generic.TemplateView):
    template_name = 'checkout.html'