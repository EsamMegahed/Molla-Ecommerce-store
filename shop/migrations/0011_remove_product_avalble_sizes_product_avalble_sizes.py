# Generated by Django 4.2.3 on 2023-08-26 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_product_avalble_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='avalble_sizes',
        ),
        migrations.AddField(
            model_name='product',
            name='avalble_sizes',
            field=models.ManyToManyField(to='shop.productsize'),
        ),
    ]