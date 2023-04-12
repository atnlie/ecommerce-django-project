from django.views import generic

from .models import ProdukItem

class HomeListView(generic.ListView):
    template_name = 'home.html'
    queryset = ProdukItem.objects.all()
    paginate_by = 4

class ProductDetailView(generic.DetailView):
    template_name = 'product_detail.html'
    queryset = ProdukItem.objects.all()

class CheckoutView(generic.TemplateView):
    template_name = 'checkout.html'