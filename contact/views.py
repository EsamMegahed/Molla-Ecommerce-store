from django.shortcuts import redirect, render
from django.core.mail import send_mail
from shop.utils import cartdata
from django.conf import settings

# Create your views here.


def contact(request):
    if request.method == "POST":
        subject = request.POST["subject"]
        email = request.POST["email"]
        message = request.POST["message"]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        return redirect("contact:contact_confirm")

    # cart items functions

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

    return render(request, "contactTemp/contact.html", context)


def contactConfirm(request):
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
    return render(request, "contactTemp/contact_message_done.html", context)
