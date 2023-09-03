import json
from .models import *


def cartdata(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order["get_cart_items"]

    # Wish LIst Functions
    if request.user.is_authenticated:
        if request.method == "POST":
            productId = request.POST.get("prouduct-id")
            product = Product.objects.get(id=productId)
            wish = WishList.objects.get_or_create(user=request.user, products=product)

        product_In_wishList = WishList.objects.filter(user=request.user)
        wishLen = len(product_In_wishList)

        PIW = []

        for i in product_In_wishList:
            PIW.append(i.products.id)

    else:
        wishLen = 0
        product_In_wishList = ""
        PIW = []

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
        "PIW": PIW,
    }

    return context
