from django.db import migrations, models

def migrate_shift_data(apps, schema_editor):
    Shift = apps.get_model('sales','Shift')
    Inventory = apps.get_model('inventory', 'Inventory')

    for shift in Shift.objects.all():
        if shift.branch_id and shift.product_id:
            # Find matching inventory instance
            try:
                inventory = Inventory.objects.get(branch_id=shift.branch_id, product_id=shift.product_id)
                
                shift.inventory = inventory
                shift.save()
            except Inventory.DoesNotExist:
                print("Inventory is empty")

class Migration(migrations.Migration):
    dependencies = [
        ('<shift>','<previous_migration_name'),
    ]

    operations = [
        migrations.RunPython(migrate_shift_data),
    ]