# Generated by Django 5.1.1 on 2024-11-13 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_rename_inventoryv_inventorysnapshot_inventory'),
        ('sales', '0003_alter_shift_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='product',
        ),
        migrations.AddField(
            model_name='shift',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_inventory', to='inventory.inventory'),
        ),
    ]
