from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from paypal.standard.forms import PayPalPaymentsForm
<<<<<<< HEAD
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
=======
from django.contrib.auth.views import redirect_to_login

>>>>>>> all_auth
from .forms import CheckoutForm, ProdukReviewForm
from .models import ProdukItem, OrderProdukItem, Order, AlamatPengiriman, Payment, ProdukImages

class KategoriListView(generic.ListView):
    def get(req, nama_kategori):
        if (nama_kategori == 'all'):
            nama = ''
            produk = ProdukItem.objects.all()
        else:
            nama = Kategori.objects.get(slug = nama_kategori)
            produk = ProductItem.objects.filter(kategori = nama)
        paginate_by = 4
        context = {
            'items' : produk
        }
        return render(self.req, 'home.html', context)

<<<<<<< HEAD
def HomeListView(req):
    # template_name = "home.html"
    produk = ProdukItem.objects.all()
    best = ProdukItem.objects.filter(label = 'BEST')
    new = ProdukItem.objects.filter(label = 'NEW')
    sale = ProdukItem.objects.filter(label = 'SALE')
    context = {
        'all' : produk,
        'best': best,
        'sale' : sale,
        'new' : new,
    }
=======
class HomeListView(generic.ListView):
    template_name = "home.html"
    queryset = ProdukItem.objects.all()
>>>>>>> all_auth
    paginate_by = 4
    return render(req, "home.html", context)

class ProductDetailView(generic.DetailView):
    template_name = "product_detail.html"
    queryset = ProdukItem.objects.all()

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['review_form'] = ProdukReviewForm()
            context['reviews'] = self.object.reviews.all()
            context['p_images'] = ProdukImages.objects.filter(produk=self.object)
            return context
      
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.object = self.get_object()
            form = ProdukReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                if request.user.is_authenticated:
                    review.user = request.user
                else:
                    # Handle anonymous user
                    review.user = AnonymousUser()
                review.produk = self.object
                review.save()
<<<<<<< HEAD
                messages.success(request, "Ulasan berhasil ditambahkan")
                return HttpResponseRedirect(request.path)
            else:
                messages.error(request, "Gagal menambahkan ulasan")
=======
                messages.success(request, "Ulasan berhasil ditambahkan.")
                return HttpResponseRedirect(request.path)
            else:
                messages.error(request, "Gagal menambahkan ulasan.")
>>>>>>> all_auth
                return self.render_to_response(self.get_context_data(form=form))
        else:
            return redirect("/accounts/login/?next=" + self.request.path)
    
    def handle_success(self, request):
        next_url = self.request.get_full_path()
        return redirect(next_url)

    def handle_authentication(self):
        return redirect("/accounts/login/?next=" + self.request.path)

class KontakView(generic.TemplateView):
<<<<<<< HEAD
    template_name = "kontak.html"
=======
    template_name = "footer.html"
>>>>>>> all_auth

class CheckoutView(LoginRequiredMixin, generic.FormView):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.produk_items.count() == 0:
                messages.warning(
                    self.request,
                    "Belum ada belajaan yang Anda pesan, lanjutkan belanja",
                )
                return redirect("toko:home-produk-list")
        except ObjectDoesNotExist:
            order = {}
            messages.warning(
                self.request, "Belum ada belajaan yang Anda pesan, lanjutkan belanja"
            )
            return redirect("toko:home-produk-list")

        context = {
            "form": form,
            "keranjang": order,
        }
        template_name = "checkout.html"
        return render(self.request, template_name, context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                alamat_1 = form.cleaned_data.get("alamat_1")
                alamat_2 = form.cleaned_data.get("alamat_2")
                negara = form.cleaned_data.get("negara")
                kode_pos = form.cleaned_data.get("kode_pos")
                opsi_pembayaran = form.cleaned_data.get("opsi_pembayaran")
                alamat_pengiriman = AlamatPengiriman(
                    user=self.request.user,
                    alamat_1=alamat_1,
                    alamat_2=alamat_2,
                    negara=negara,
                    kode_pos=kode_pos,
                )

                alamat_pengiriman.save()
                order.alamat_pengiriman = alamat_pengiriman
                order.save()
                if opsi_pembayaran == "P":
                    return redirect("toko:payment", payment_method="paypal")
                else:
                    return redirect("toko:payment", payment_method="stripe")

            messages.warning(self.request, "Gagal checkout")
            return redirect("toko:checkout")
        except ObjectDoesNotExist:
            messages.error(self.request, "Tidak ada pesanan yang aktif")
            return redirect("toko:order-summary")


class PaymentView(LoginRequiredMixin, generic.FormView):
    template_name = "payment.html"
    
    def get(self, *args, **kwargs):
        template_name = "payment.html"
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            paypal_data = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": order.get_total_harga_order,
                "item_name": f"Pembayaran belajanan order: {order.id}",
                "invoice": f"{order.id}-{timezone.now().timestamp()}",
                "currency_code": "USD",
                "notify_url": self.request.build_absolute_uri(reverse("paypal-ipn")),
                "return_url": self.request.build_absolute_uri(
                    reverse("toko:paypal-return")
                ),
                "cancel_return": self.request.build_absolute_uri(
                    reverse("toko:paypal-cancel")
                ),
            }

            qPath = self.request.get_full_path()
            isPaypal = "paypal" in qPath

            form = PayPalPaymentsForm(initial=paypal_data)
            context = {
                "paypalform": form,
                "order": order,
                "is_paypal": isPaypal,
            }
            return render(self.request, template_name, context)

        except ObjectDoesNotExist:
            return redirect("toko:checkout")
    
def checkout_stripe(request):
            order = Order.objects.get(user=request.user, ordered=False)
            price = int(order.get_total_harga_order() * 100)
            checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                        "price_data": {
                                        "currency": "usd",
                                        "unit_amount": price,
                                        "product_data": {
                                            "name": "Pembayaran belanjaan",
                                        },
                                    },
                                    "quantity": 1,
                                }
                            ],
                    mode="payment",
                    success_url = 'http://127.0.0.1:8000/stripe-success/',
                    cancel_url = 'http://127.0.0.1:8000/stripe-cancel/'
            )
            return redirect(checkout_session.url, code=303)

class OrderSummaryView(LoginRequiredMixin, generic.TemplateView):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"keranjang": order}
            template_name = "order_summary.html"
            return render(self.request, template_name, context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Tidak ada pesanan yang aktif")
            return redirect("toko:produk-detail")

def add_to_cart(request, slug):
    if request.user.is_authenticated:
        produk_item = get_object_or_404(ProdukItem, slug=slug)
        order_produk_item, created = OrderProdukItem.objects.get_or_create(
            produk_item=produk_item, 
            user=request.user, 
            ordered=False
<<<<<<< HEAD
        )
        order_query = Order.objects.filter(
            user=request.user, 
            ordered=False
        )

=======
        )
        order_query = Order.objects.filter(
            user=request.user, 
            ordered=False
        )
>>>>>>> all_auth
        if order_query.exists():
            order = order_query[0]

            if order.produk_items.filter(produk_item=produk_item).exists():
                order_produk_item.quantity += 1
                order_produk_item.save()
                pesan = f"Produk item sudah diupdate menjadi: {order_produk_item.quantity}"
                messages.info(request, pesan)
            else:
                order.produk_items.add(order_produk_item)
                messages.info(request, "Produk item pilihanmu sudah ditambahkan")
<<<<<<< HEAD
                return redirect("toko:produk-detail", slug=slug)
=======
>>>>>>> all_auth
        else:
            tanggal_order = timezone.now()
            order = Order.objects.create(
                user=request.user, 
<<<<<<< HEAD
                tanggal_order=tanggal_order
            )
=======
                tanggal_order=tanggal_order)
>>>>>>> all_auth
            order.produk_items.add(order_produk_item)
            messages.info(request, "Produk item pilihanmu sudah ditambahkan")
        total_produk = order.produk_items.count()
        request.session['total_produk_dikeranjang'] = total_produk
        return redirect("toko:order-summary")
    else:
        return redirect("/accounts/login")
        
def remove_single_item_from_cart(request, slug):
    if request.user.is_authenticated:
        produk_item = get_object_or_404(ProdukItem, slug=slug)
        order_query = Order.objects.filter(
            user=request.user, 
            ordered=False
        )

        if order_query.exists():
            order = order_query[0]

            if order.produk_items.filter(produk_item=produk_item).exists():
                order_produk_item = OrderProdukItem.objects.filter(
                    produk_item=produk_item, 
                    user=request.user, 
                    ordered=False
                )[0]
                if order_produk_item.quantity > 1:
                    order_produk_item.quantity -= 1
                    order_produk_item.save()
                else:
                    order.produk_items.remove(order_produk_item)
                messages.info(request, "Produk item dihapus dari keranjang")
<<<<<<< HEAD
=======
                return redirect("toko:order-summary")
            else:
                messages.info(request, "Produk item tidak ada")
>>>>>>> all_auth
                return redirect("toko:order-summary")
            else:
                messages.info(request, "Produk item tidak ada")
                return redirect("toko:produk-detail", slug=slug)
        else:
            messages.info(request, "Tidak ada order yang aktif")
<<<<<<< HEAD
            return redirect("toko:produk-detail")
=======
            return redirect("toko:order-summary")
>>>>>>> all_auth
    else:
        return redirect("/accounts/login")

def remove_from_cart(request, slug):
    if request.user.is_authenticated:
        produk_item = get_object_or_404(ProdukItem, slug=slug)
        order_query = Order.objects.filter(user=request.user, ordered=False)
        if order_query.exists():
            order = order_query[0]
            
            if order.produk_items.filter(produk_item__slug=produk_item.slug).exists():
                order_produk_item = OrderProdukItem.objects.filter(
<<<<<<< HEAD
                        produk_item=produk_item, 
                        user=request.user, 
                        ordered=False
                    ).first()
                
=======
                        produk_item=produk_item, user=request.user, ordered=False
                    ).first()
>>>>>>> all_auth
                order.produk_items.remove(order_produk_item)
                order_produk_item.delete()
                pesan = "Semua produk item dihapus dari keranjang"
                messages.info(request, pesan)
                return redirect("toko:order-summary")
            else:
                messages.info(request, "Produk item tidak ada")
                return redirect("toko:produk-detail")
        else:
            messages.info(request, "Produk item tidak ada order yang aktif")
            return redirect("toko:produk-detail")
    else:
        return redirect("/accounts/login")
    
# @csrf_exempt
def paypal_return(request):
    if request.user.is_authenticated:
        try:
            print("paypal return", request)
            order = Order.objects.get(user=request.user, ordered=False)
            payment = Payment()
            payment.user = request.user
            payment.amount = order.get_total_harga_order()
            payment.payment_option = "P"  # paypal kalai 'S' stripe
            payment.charge_id = f"{order.id}-{timezone.now()}"
            payment.timestamp = timezone.now()
            payment.save()

            order_produk_item = OrderProdukItem.objects.filter(
                user=request.user, ordered=False
            )
            order_produk_item.update(ordered=True)

            order.payment = payment
            order.ordered = True
            order.save()

            messages.info(request, "Pembayaran sudah diterima, terima kasih")
            return redirect("toko:home-produk-list")
        except ObjectDoesNotExist:
            messages.error(request, "Periksa kembali pesananmu")
            return redirect("toko:order-summary")
    else:
        return redirect("/accounts/login")


# @csrf_exempt
def paypal_cancel(request):
    messages.error(request, "Pembayaran dibatalkan")
    return redirect("toko:order-summary")

<<<<<<< HEAD
def stripe_success(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            payment = Payment()
            payment.user = request.user
            payment.amount = order.get_total_harga_order()
            payment.payment_option = "S"  # 'P' untuk Paypal, 'S' untuk Stripe
            payment.charge_id = f"{order.id}-{timezone.now()}"
            payment.timestamp = timezone.now()
            payment.save()

            order_produk_item = OrderProdukItem.objects.filter(
                user=request.user, ordered=False
            )
            order_produk_item.update(ordered=True)

            order.payment = payment
            order.ordered = True
            order.save()

            messages.info(request, "Pembayaran sudah diterima, terima kasih")
            return redirect("toko:home-produk-list")
        except ObjectDoesNotExist:
            messages.error(request, "Periksa kembali pesananmu")
            return redirect("toko:order-summary")
    else:
        return redirect("/accounts/login")


def stripe_cancel(request):
    messages.error(request, "Pembayaran dibatalkan")
    return redirect("toko:checkout")

=======
>>>>>>> all_auth

