from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
)

app_name = "toko"

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home-produk-list"),
    path("product/<slug>/", views.ProductDetailView.as_view(), name="produk-detail"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("kontak/", views.KontakView.as_view(), name="kontak"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>/", remove_from_cart, name="remove-from-cart"),
    path("order-summary/", views.OrderSummaryView.as_view(), name="order-summary"),
    path("payment/<payment_method>", views.PaymentView.as_view(), name="payment"),
    path("paypal-return/", views.paypal_return, name="paypal-return"),
    path("paypal-cancel/", views.paypal_cancel, name="paypal-cancel"),
    path("remove-single-item-from-cart/<slug>/", remove_single_item_from_cart, name="remove-single-item-from-cart"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
