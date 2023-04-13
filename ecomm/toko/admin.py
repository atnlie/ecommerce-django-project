from django.contrib import admin
from .models import ProdukItem, OrderProdukItem, Order, AlamatPengiriman, Payment

class ProdukItemAdmin(admin.ModelAdmin):
    list_display = ['nama_produk','harga', 'harga_diskon', 'slug',
                    'deskripsi', 'gambar', 'label', 'kategori']

class OrderProdukItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'produk_item', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'tanggal_mulai', 'tanggal_order', 'ordered']

class AlamatPengirimanAdmin(admin.ModelAdmin):
    list_display = ['user', 'alamat_1', 'alamat_2', 'kode_pos', 'negara']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp', 'payment_option', 'charge_id']

admin.site.register(ProdukItem, ProdukItemAdmin)
admin.site.register(OrderProdukItem, OrderProdukItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(AlamatPengiriman, AlamatPengirimanAdmin)
admin.site.register(Payment, PaymentAdmin)
