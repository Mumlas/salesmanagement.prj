# Generated by Django 5.1.1 on 2024-10-31 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('dateUpdated', models.DateField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_product', to='setup.product')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.storage')),
                ('updatedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.staff')),
            ],
            options={
                'verbose_name_plural': 'Inventory',
            },
        ),
        migrations.CreateModel(
            name='InventorySnapShot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date', models.DateField()),
                ('inventoryv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.product')),
            ],
            options={
                'verbose_name_plural': 'Inventory',
            },
        ),
    ]
