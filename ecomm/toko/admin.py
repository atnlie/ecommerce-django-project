from django.contrib import admin
from .models import ProdukItem, OrderProdukItem, Order, AlamatPengiriman, Payment, Kategori, ProdukReview, ProdukImages

class ProdukReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'nama', 'produk', 'rating','komentar', 'publish', 'status']

class KategoriAdmin(admin.ModelAdmin):
    list_display = ['nama_kategori', 'slug']
    prepopulated_fields = {'slug' : ('nama_kategori',)}

class ProdukImagesAdmin(admin.TabularInline):
    model = ProdukImages

class ProdukItemAdmin(admin.ModelAdmin):
    inlines = [ProdukImagesAdmin]
    list_display = ['nama_produk','harga', 'harga_diskon', 'slug',
                    'deskripsi', 'detail_produk', 'gambar', 'label', 'kategori', 'pid']
    prepopulated_fields = {"slug": ("nama_produk",)}

class OrderProdukItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'produk_item', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'tanggal_mulai', 'tanggal_order', 'ordered']

class AlamatPengirimanAdmin(admin.ModelAdmin):
    list_display = ['user', 'alamat_1', 'alamat_2', 'kode_pos', 'negara']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp', 'payment_option', 'charge_id']

admin.site.register(Kategori, KategoriAdmin)
admin.site.register(ProdukItem, ProdukItemAdmin)
admin.site.register(OrderProdukItem, OrderProdukItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(AlamatPengiriman, AlamatPengirimanAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ProdukReview,ProdukReviewAdmin)
