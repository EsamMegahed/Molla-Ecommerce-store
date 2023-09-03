from django.shortcuts import render
from shop.utils import cartdata

# Create your views here.


def aboutUs(request):
    data = cartdata(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    wishLen = data["wishLen"]
    product_In_wishList = data["product_In_wishList"]
    PIW = data["PIW"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
        "PIW": PIW,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
    }
    return render(request, "about_page/about_us.html", context)
