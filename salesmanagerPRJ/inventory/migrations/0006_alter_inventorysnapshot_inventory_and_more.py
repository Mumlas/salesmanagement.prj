# Generated by Django 5.1.1 on 2024-12-05 08:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventorysnapshot_options_and_more'),
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorysnapshot',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.inventory'),
        ),
        migrations.AlterField(
            model_name='inventorysnapshot',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='setup.product'),
        ),
    ]
