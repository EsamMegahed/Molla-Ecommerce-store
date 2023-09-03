from django import forms
from .models import *


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        exclude = ["customer", "order"]
