from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from .models import ProdukItem, OrderProdukItem, Order

class HomeListView(generic.ListView):
    template_name = 'home.html'
    queryset = ProdukItem.objects.all()
    paginate_by = 4

class ProductDetailView(generic.DetailView):
    template_name = 'product_detail.html'
    queryset = ProdukItem.objects.all()

class CheckoutView(generic.TemplateView):
    template_name = 'checkout.html'


def add_to_cart(request, slug):
    produk_item = get_object_or_404(ProdukItem, slug=slug)
    order_produk_item, _ = OrderProdukItem.objects.get_or_create(
        produk_item=produk_item,
        user=request.user,
        ordered=False
    )
    order_query = Order.objects.filter(user=request.user, ordered=False)
    if order_query.exists():
        order = order_query[0]
        if order.produk_items.filter(produk_item__slug=produk_item.slug).exists():
            order_produk_item.quantity += 1
            order_produk_item.save()
            pesan = f"ProdukItem sudah diupdate menjadi: { order_produk_item.quantity }"
            messages.info(request, pesan)
            return redirect('toko:produk-detail', slug = slug)
        else:
            order.produk_items.add(order_produk_item)
            messages.info(request, 'ProdukItem pilihanmu sudah ditambahkan')
            return redirect('toko:produk-detail', slug = slug)
    else:
        tanggal_order = timezone.now()
        order = Order.objects.create(user=request.user, tanggal_order=tanggal_order)
        order.produk_items.add(order_produk_item)
        messages.info(request, 'ProdukItem pilihanmu sudah ditambahkan')
        return redirect('toko:produk-detail', slug = slug)
