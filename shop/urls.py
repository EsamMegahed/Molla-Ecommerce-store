from django.urls import path, include
from . import views


urlpatterns = [
    path("store/", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="updateItem"),
    path("wish_list/", views.myWishList, name="wishList"),
    path("<str:slug>", views.productDetails, name="product_details"),
    path("", views.home, name="home"),
]
