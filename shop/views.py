from django.shortcuts import redirect, render
from django.http import JsonResponse
import json

from django.urls import reverse
from .models import *
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .filters import ProductFilter
from .forms import ShippingForm

from .utils import cartdata

# Create your views here.


def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        data = cartdata(request)
        cartItems = data["cartItems"]
        items = data["items"]
        order = data["order"]
        wishLen = data["wishLen"]
        product_In_wishList = data["product_In_wishList"]
        PIW = data["PIW"]
    else:
        my_list = 0
        cartItems = 0
        items = []
        order = []
        wishLen = 0
        product_In_wishList = []
        PIW = []

    ## Filters

    myfilter = ProductFilter(request.GET, queryset=products)
    productsa = myfilter.qs

    paginator = Paginator(productsa, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_len = len(page_obj.paginator.page_range)

    profile = Profile.objects.all()

    context = {
        "page_len": page_len,
        "products": page_obj,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
        "profile": profile,
        "productsa": products,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
        "PIW": PIW,
        "myfilter": myfilter,
        "page_number": page_number,
    }
    return render(request, "shop/store.html", context)


@login_required
def cart(request):
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
    return render(request, "shop/cart.html", context)


@login_required
def checkout(request):
    # shipping System
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        if request.method == "POST":
            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False
            )

            shipp_form = ShippingForm(request.POST)
            if shipp_form.is_valid() and int(order.get_cart_total) != 0:
                order.transaction_id = transaction_id
                order.complete = True
                order.save()

                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    full_Name=shipp_form.cleaned_data["full_Name"],
                    email_address=shipp_form.cleaned_data["email_address"],
                    country=shipp_form.cleaned_data["country"],
                    state=shipp_form.cleaned_data["state"],
                    town=shipp_form.cleaned_data["town"],
                    addressOne=shipp_form.cleaned_data["addressOne"],
                    addressTwo=shipp_form.cleaned_data["addressTwo"],
                    zipcode=shipp_form.cleaned_data["zipcode"],
                    text_erea=shipp_form.cleaned_data["text_erea"],
                )
                return redirect(reverse("store"))
            else:
                return redirect(reverse("checkout"))

        else:
            form = ShippingForm()

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
        "form": form,
    }
    return render(request, "shop/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    wish_list = WishList.objects.filter(products=productId, user=request.user)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if action == "remove-product" or orderItem.quantity <= 0:
        orderItem.delete()

    if action == "remove-wishlist":
        wish_list.delete()

    return JsonResponse("item was add", safe=False)


@login_required
def myWishList(request):
    my_list = WishList.objects.filter(user=request.user)
    data = cartdata(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    wishLen = data["wishLen"]
    product_In_wishList = data["product_In_wishList"]
    PIW = data["PIW"]

    context = {
        "my_list": my_list,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
        "PIW": PIW,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
    }
    return render(request, "shop/wishlist.html", context)


def productDetails(request, slug):
    # Prouduct code
    product_slug = Product.objects.get(slug=slug)
    size = product_slug.avalble_sizes.all()
    color = product_slug.avalble_color.all()
    brand = product_slug.product_Brand.all()

    # wish list code
    if request.user.is_authenticated:
        my_list = WishList.objects.filter(user=request.user)
        data = cartdata(request)
        cartItems = data["cartItems"]
        items = data["items"]
        order = data["order"]
        wishLen = data["wishLen"]
        product_In_wishList = data["product_In_wishList"]
        PIW = data["PIW"]
    else:
        my_list = 0
        cartItems = 0
        items = []
        order = []
        wishLen = 0
        product_In_wishList = []
        PIW = []

    context = {
        "product_slug": product_slug,
        "size": size,
        "color": color,
        "brand": brand,
        "my_list": my_list,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
        "PIW": PIW,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
    }
    return render(request, "shop/product_details.html", context)


def home(request):
    if request.user.is_authenticated:
        my_list = WishList.objects.filter(user=request.user)
        data = cartdata(request)
        cartItems = data["cartItems"]
        items = data["items"]
        order = data["order"]
        wishLen = data["wishLen"]
        product_In_wishList = data["product_In_wishList"]
        PIW = data["PIW"]
    else:
        my_list = 0
        cartItems = 0
        items = []
        order = []
        wishLen = 0
        product_In_wishList = []
        PIW = []
    context = {
        "my_list": my_list,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "PIW": PIW,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
    }

    return render(request, "shop/home.html", context)
