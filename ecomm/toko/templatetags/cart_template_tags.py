from django import template
from toko.models import OrderProdukItem
from django.db.models import Sum

register = template.Library()

@register.filter
def total_produk_dikeranjang(user):
    if user.is_authenticated:
        query = OrderProdukItem.objects.filter(user=user, ordered=False)
        if query.exists():
            total_quantity = OrderProdukItem.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
            return total_quantity
            
    return 0
