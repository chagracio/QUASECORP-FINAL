# Generated by Django 4.0.3 on 2022-05-12 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='RiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField(blank=True)),
                ('image', models.ImageField(null=True, upload_to='rice_images/')),
            ],
        ),
        migrations.CreateModel(
            name='OrderRiceItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.order')),
                ('rice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.riceitem')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('address', models.CharField(max_length=200, null=True)),
                ('ContactNum', models.CharField(blank=True, max_length=11, null=True)),
                ('shippingMeth', models.CharField(max_length=15, null=True)),
                ('shippingStatus', models.CharField(blank=True, choices=[('Preparing', 'Owner is preparing your order'), ('Out for delivery', 'Your order is out for delivery'), ('Delivered', 'Order Delivered'), ('Ready for Pick Up', 'Your order is ready for pick up'), ('Picked Up', 'Order Picked Up')], max_length=50)),
                ('orderStatus', models.CharField(blank=True, choices=[('Accepted', 'Accepted'), ('Denied', 'Denied')], max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.order')),
                ('rice_ordered', models.ManyToManyField(blank=True, related_name='orders', to='customer.orderriceitems')),
            ],
        ),
        migrations.CreateModel(
            name='LendingStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContactNum', models.CharField(blank=True, max_length=11, null=True)),
                ('total_payment', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('status', models.CharField(blank=True, max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
            ],
        ),
    ]
