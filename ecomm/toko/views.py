from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
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
    def get(self, *args, **kwargs):
        # form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.produk_items.count() == 0:
                messages.warning(self.request, 'Belum ada belajaan yang Anda pesan, lanjutkan belanja')
                return redirect('toko:home-produk-list')
        except ObjectDoesNotExist:
            order = {}
            messages.warning(self.request, 'Belum ada belajaan yang Anda pesan, lanjutkan belanja')
            return redirect('toko:home-produk-list')

        context = {
            # 'form': form,
            'keranjang': order,
        }
        template_name = 'checkout.html'
        return render(self.request, template_name, context)


class OrderSummaryView(generic.TemplateView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'keranjang': order
            }
            template_name = 'order_summary.html'
            return render(self.request, template_name, context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Tidak ada pesanan yang aktif')
            return redirect('/')


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

def remove_from_cart(request, slug):
    produk_item = get_object_or_404(ProdukItem, slug=slug)
    order_query = Order.objects.filter(
        user=request.user, ordered=False
    )
    if order_query.exists():
        order = order_query[0]
        if order.produk_items.filter(produk_item__slug=produk_item.slug).exists():
           try: 
                order_produk_item = OrderProdukItem.objects.filter(
                    produk_item=produk_item,
                    user=request.user,
                    ordered=False
                )[0]
                
                order.produk_items.remove(order_produk_item)
                order_produk_item.delete()

                pesan = f"ProdukItem sudah dihapus"
                messages.info(request, pesan)
                return redirect('toko:produk-detail',slug = slug)
           except ObjectDoesNotExist:
               print('Error: order ProdukItem sudah tidak ada')
        else:
            messages.info(request, 'ProdukItem tidak ada')
            return redirect('toko:produk-detail',slug = slug)
    else:
        messages.info(request, 'ProdukItem tidak ada order yang aktif')
        return redirect('toko:produk-detail',slug = slug)