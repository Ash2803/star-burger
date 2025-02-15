import json

from django.http import JsonResponse
from django.templatetags.static import static


from .models import Product, Order, OrderProduct


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    order_info = json.loads(request.body.decode())
    order = Order.objects.create(
        client_name=f'{order_info["firstname"]} {order_info["lastname"]}',
        client_number=order_info['phonenumber'],
        delivery_address=order_info['address'],
    )
    order_products = []
    for product in order_info['products']:
        product_id = product.get('product')
        quantity = product.get('quantity')
        product = Product.objects.get(id=product_id)
        order_products.append(OrderProduct(
            order=order,
            product=product,
            quantity=quantity,
        ))
    OrderProduct.objects.bulk_create(order_products)
    return JsonResponse({})
