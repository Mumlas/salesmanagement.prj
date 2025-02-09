# Generated by Django 5.1.1 on 2024-11-14 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_inventory_dateupdated_and_more'),
        ('sales', '0009_remove_shift_is_active_shift_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shift_inventory', to='inventory.inventory'),
        ),
    ]
