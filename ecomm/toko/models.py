from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
import datetime

PILIHAN_KATEGORI = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

PILIHAN_LABEL = (
    ('NEW', 'New'),
    ('SALE', 'Sale'),
    ('BEST', 'Bestseller'),
)

PILIHAN_PEMBAYARAN = (
    ('P', 'Paypal'),
    ('S', 'Stripe'),
)

PILIHAN_RATING = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

User = get_user_model()

class Kategori(models.Model):
    nama_kategori = models.CharField(choices=PILIHAN_KATEGORI, max_length=2)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.nama_kategori

class ProdukItem(models.Model):
    nama_produk = models.CharField(max_length=100)
    harga = models.IntegerField()
    harga_diskon = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    deskripsi = models.TextField()
    detail_produk = models.TextField(null=True)
    gambar = models.ImageField(upload_to='product_pics')
    label = models.CharField(choices=PILIHAN_LABEL, max_length=11)
    #kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    kategori = models.CharField(choices=PILIHAN_KATEGORI, max_length=2)
    
    @property
    def pid(self):
        return self.id
    
    def __str__(self):
        return f"{self.nama_produk} - Rp. {self.harga},-"
    
    def get_absolute_url(self):
        return reverse("toko:produk-detail", kwargs={
            "slug": self.slug
            })

    def get_add_to_cart_url(self):
        return reverse("toko:add-to-cart", kwargs={
            "slug": self.slug
            })
    
    def get_remove_from_cart_url(self):
        return reverse("toko:remove-from-cart", kwargs={
            "slug": self.slug
            })
    
    def get_remove_single_item_from_cart_url(self):
        return reverse("toko:remove-single-item-from-cart", kwargs={
            "slug": self.slug
            })

class ProdukImages(models.Model):
    produk = models.ForeignKey(ProdukItem, related_name="p_images", on_delete=models.SET_NULL, null=True)
    images = models.ImageField(upload_to='product-images',default="product.jpg")

    class Meta :
        verbose_name_plural =  "Product Images"

    def __str__(self):
        return f"Gambar Produk {self.produk}"

class OrderProdukItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    produk_item = models.ForeignKey(ProdukItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.produk_item.nama_produk}"

    def get_total_harga_item(self):
        return self.quantity * self.produk_item.harga
    
    def get_total_harga_diskon_item(self):
        return self.quantity * self.produk_item.harga_diskon

    def get_total_hemat_item(self):
        return self.get_total_harga_item() - self.get_total_harga_diskon_item()
    
    def get_total_item_keseluruan(self):
        if self.produk_item.harga_diskon:
            return self.get_total_harga_diskon_item()
        return self.get_total_harga_item()
    
    def get_total_hemat_keseluruhan(self):
        if self.produk_item.harga_diskon:
            return self.get_total_hemat_item()
        return 0

class ProdukReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produk = models.ForeignKey(ProdukItem, on_delete=models.CASCADE, related_name='reviews')
    nama = models.CharField(max_length=50, default='Anonymous')
    komentar = models.TextField()
    publish = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(default=True)
    rating = models.CharField(choices=PILIHAN_RATING, max_length=2)

    class Meta:
        ordering = ("publish",)

    def __str__(self):
        return f"Comment by {self.nama}"
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    produk_items = models.ManyToManyField(OrderProdukItem)
    tanggal_mulai = models.DateTimeField(auto_now_add=True)
    tanggal_order = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    alamat_pengiriman = models.ForeignKey('AlamatPengiriman', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
         
    def get_total_harga_order(self):
        total = 0
        for order_produk_item in self.produk_items.all():
            total += order_produk_item.get_total_item_keseluruan()
        return total
    
    def get_total_hemat_order(self):
        total = 0
        for order_produk_item in self.produk_items.all():
            total += order_produk_item.get_total_hemat_keseluruhan()
        return total

class AlamatPengiriman(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alamat_1 = models.CharField(max_length=100)
    alamat_2 = models.CharField(max_length=100)
    negara = models.CharField(max_length=100)
    kode_pos = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.alamat_1}"

    class Meta:
        verbose_name_plural = 'AlamatPengiriman'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_option = models.CharField(choices=PILIHAN_PEMBAYARAN, max_length=1)
    charge_id = models.CharField(max_length=50)

    def __self__(self):
        return self.user.username
    
    def __str__(self):
        return f"{self.user.username} - {self.payment_option} - {self.amount}"
    
    class Meta:
        verbose_name_plural = 'Payment'