from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.name


class ProductSize(models.Model):
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.size


class ProductColor(models.Model):
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.size


class ProductBrand(models.Model):
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.size


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=300, null=True)
    descriptions = models.TextField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(
        null=True,
        blank=True,
    )
    avalble_sizes = models.ManyToManyField(ProductSize)
    avalble_color = models.ManyToManyField(ProductColor)
    product_Brand = models.ManyToManyField(ProductBrand)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **keywargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **keywargs)

    def __str__(self) -> str:
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""

        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        return shipping

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])

        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity

        return total

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    full_Name = models.CharField(max_length=200, null=True, blank=True)
    email_address = models.EmailField()
    country = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    town = models.CharField(max_length=50, null=True)
    addressOne = models.CharField(max_length=200, null=True)
    addressTwo = models.CharField(max_length=200, null=True)

    zipcode = models.CharField(max_length=20, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    text_erea = models.TextField(max_length=1500)

    def __str__(self) -> str:
        return self.addressOne


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.products)
