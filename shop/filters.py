from .models import Product
import django_filters


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    descriptions = django_filters.CharFilter(lookup_expr="icontains")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")

    class Meta:
        model = Product
        fields = "__all__"
        exclude = [
            "image",
            "avalble_color",
            "slug",
            "product_Brand",
            "title",
            "price",
        ]
