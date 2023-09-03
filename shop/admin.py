from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductBrand)
admin.site.register(ShippingAddress)
admin.site.register(WishList)
admin.site.register(Category)