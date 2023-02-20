# Generated by Django 3.2.15 on 2023-02-20 13:49

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20230216_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(db_index=True, max_length=100, verbose_name='Client name')),
                ('client_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('delivery_address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Order date')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]