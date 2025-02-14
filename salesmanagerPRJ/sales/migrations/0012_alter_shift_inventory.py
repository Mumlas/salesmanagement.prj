# Generated by Django 5.1.1 on 2024-12-05 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_inventorysnapshot_product_and_more'),
        ('sales', '0011_alter_sales_reconciliation_alter_shift_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shift_inventory', to='inventory.inventory'),
        ),
    ]
