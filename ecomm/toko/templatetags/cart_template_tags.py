from django import template
from toko.models import Order

register = template.Library()

@register.filter
def total_produk_dikeranjang(user):
    if user.is_authenticated:
        query = Order.objects.filter(user=user, ordered=False)
        if query.exists():
            return query[0].produk_items.count()
    return 0
