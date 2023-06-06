from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = "toko"

urlpatterns = [
    path("", views.HomeListView, name="home-produk-list"),
    path("product/<slug>/", views.ProductDetailView.as_view(), name="produk-detail"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("kontak/", views.KontakView.as_view(), name="kontak"),
    path("add-to-cart/<slug>/", views.add_to_cart, name="add-to-cart"),
    path("remove_from_cart/<slug>/", views.remove_from_cart, name="remove-from-cart"),
    path("order-summary/", views.OrderSummaryView.as_view(), name="order-summary"),
    path("payment/<payment_method>", views.PaymentView.as_view(), name="payment"),
    path("paypal-return/", views.paypal_return, name="paypal-return"),
    path("paypal-cancel/", views.paypal_cancel, name="paypal-cancel"),
    path('hapus-produk/<int:item_id>/', views.hapus_produk, name='hapus-produk'),
    path("remove-single-item-from-cart/<slug>/", views.remove_single_item_from_cart, name="remove-single-item-from-cart"),
]

urlpatterns += staticfiles_urlpatterns()
