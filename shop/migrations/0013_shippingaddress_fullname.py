# Generated by Django 4.2.3 on 2023-08-30 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_product_avalble_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='fullName',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
