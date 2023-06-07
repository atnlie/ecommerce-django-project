from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "toko"

urlpatterns = [
    path("", views.HomeListView, name="home-produk-list"),
    path("product/<slug>/", views.ProductDetailView.as_view(), name="produk-detail"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("kontak/", views.KontakView.as_view(), name="kontak"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", views.remove_from_cart, name="remove-from-cart"),
    path("order-summary/", views.OrderSummaryView.as_view(), name="order-summary"),
    path("payment/<payment_method>", views.PaymentView.as_view(), name="payment"),
    path("paypal-return/", views.paypal_return, name="paypal-return"),
    path("paypal-cancel/", views.paypal_cancel, name="paypal-cancel"),
    path("remove-single-item-from-cart/<slug>/", views.remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path("stripe-success/", views.stripe_success, name="stripe-success"),
    path("stripe-cancel/", views.stripe_cancel, name="stripe-cancel"),
    path("checkout-stripe/", views.checkout_stripe, name="checkout-stripe"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
