# Generated by Django 5.1.6 on 2025-02-25 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_farmer_order_products_product_farmer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='razorpay_order_id',
        ),
    ]
