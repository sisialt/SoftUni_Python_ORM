import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
import populate_db
from django.db.models import Q, Count, Sum, F


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    query_full_name = Q(full_name__icontains=search_string)
    query_email = Q(email__icontains=search_string)
    query_phone_number = Q(phone_number__icontains=search_string)

    profiles = Profile.objects.annotate(
        num_orders=Count('orders')
    ).filter(
        query_full_name | query_email | query_phone_number
    ).order_by('full_name')

    if not profiles:
        return ""

    result = []

    for p in profiles:
        result.append(f"Profile: {p.full_name}, "
                      f"email: {p.email}, "
                      f"phone number: {p.phone_number}, "
                      f"orders: {p.num_orders}")

    return '\n'.join(result)

# def get_profiles(search_string: str = None) -> str:
#     if search_string is None:
#         return ""
#
#     profiles = Profile.objects.filter(
#         Q(full_name__icontains=search_string)
#             |
#         Q(email__icontains=search_string)
#             |
#         Q(phone_number__icontains=search_string)
#     ).order_by('full_name')
#
#     return "\n".join(
#         f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.orders.count()}"
#         for p in profiles
#     )


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ""

    result = []

    for p in profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.num_orders}")

    return '\n'.join(result)

# def get_loyal_profiles() -> str:
#     profiles = Profile.objects.get_regular_customers()
#
#     return "\n".join(
#         f"Profile: {p.full_name}, orders: {p.orders_count}"
#         for p in profiles
#     )


def get_last_sold_products():
    last_order = Order.objects.order_by('-creation_date').first()

    if not last_order or not last_order.products.all():
        return ""

    products = last_order.products.order_by('name')

    return f"Last sold products: {', '.join([p.name for p in products])}"

# def get_last_sold_products() -> str:
#     last_order = Order.objects.prefetch_related('products').last()
#
#     if last_order is None or not last_order.products.exists():
#         return ""
#
#     product_names = [product.name for product in last_order.products.all()]
#
#     return f"Last sold products: {', '.join(product_names)}"

def get_top_products() -> str:
    top_products = Product.objects.annotate(
        orders_count=Count('orders')
    ).filter(
        orders_count__gt=0
    ).order_by(
        '-orders_count',
        'name'
    )[:5]

    if not top_products:
        return ""

    product_lines = [f"{p.name}, sold {p.orders_count} times" for p in top_products]

    return f"Top products:\n" + "\n".join(product_lines)
# def get_top_products():
#     if not Order.objects.all():
#         return ""
#
#     products = Product.objects.annotate(
#         num_orders=Count('orders')
#     ).filter(
#         num_orders__gt=0
#     ).order_by(
#         '-num_orders', 'name'
#     )[:5]
#     if not products:
#         return ""
#
#     result = ["Top products:"]
#
#     for p in products:
#         result.append(f"{p.name}, sold {p.num_orders} times")
#
#     return '\n'.join(result) # problem with formating the end result


def apply_discounts():
    orders = Order.objects.annotate(num_products=Count('products')).filter(is_completed=False, num_products__gt=2) #forgot >2
    if not orders:
        num_of_updated_orders = 0
    else:
        num_of_updated_orders = orders.update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."

# def apply_discounts() -> str:
#     updated_orders_count = Order.objects.annotate(
#         products_count=Count('products')
#     ).filter(
#         products_count__gt=2,
#         is_completed=False,
#     ).update(
#         total_price=F('total_price') * 0.90
#     )
#
#     return f"Discount applied to {updated_orders_count} orders."


def complete_order():
    if not Order.objects.all() or not Order.objects.filter(is_completed=False):
        return ""

    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()
    order.is_completed = True

    for p in order.products.all():
        if p.is_available:
            p.in_stock -= 1
            if p.in_stock == 0:
                p.is_available = False
            p.save()

    order.save()

    return "Order has been completed!"

# def complete_order() -> str:
#     order = Order.objects.prefetch_related('products').filter(
#         is_completed=False
#     ).order_by(
#         'creation_date'
#     ).first()
#
#     if not order:
#         return ""
#
#     for product in order.products.all():
#         product.in_stock -= 1
#
#         if product.in_stock == 0:
#             product.is_available = False
#
#         product.save()
#
#     order.is_completed = True
#     order.save()
#
#     return f"Order has been completed!"

populate_db.populate_model_with_data(Order, 5)
