from django.urls import path, include
from . import views


app_name = "about_us"

urlpatterns = [
    path("", views.aboutUs, name="about_us_in"),
]
