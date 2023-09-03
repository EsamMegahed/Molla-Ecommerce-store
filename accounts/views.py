from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from .models import Profile
from django.contrib.auth.decorators import login_required
from shop.models import *
from shop.utils import cartdata
from django.contrib.auth.models import User

# Create your views here.


def signUp(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            login(request, user)
            Customer.objects.create(
                user=request.user,
                name=first_name,
                email=email,
            )
            return redirect("store")
    else:
        form = SignUpForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


@login_required
def profile(request):
    profile = Profile.objects.get(
        user=request.user,
    )
    image = profile.image_URL

    products = Product.objects.all()
    data = cartdata(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    wishLen = data["wishLen"]
    product_In_wishList = data["product_In_wishList"]
    PIW = data["PIW"]

    context = {
        "profile": profile,
        "products": products,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
        "PIW": PIW,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
        "image": image,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        userForm = UserForm(request.POST, instance=request.user)
        profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            myprfile = profileForm.save(commit=False)
            myprfile.user = request.user
            myprfile.save()
            return redirect(reverse("accounts:profile"))

    else:
        userForm = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=profile)

    # Product items
    my_list = WishList.objects.filter(user=request.user)
    data = cartdata(request)
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]
    wishLen = data["wishLen"]
    product_In_wishList = data["product_In_wishList"]
    PIW = data["PIW"]

    context = {
        "userForm": userForm,
        "profileForm": profileForm,
        "my_list": my_list,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
        "PIW": PIW,
        "wishLen": wishLen,
        "product_In_wishList": product_In_wishList,
    }

    return render(request, "accounts/profile_edit.html", context)
