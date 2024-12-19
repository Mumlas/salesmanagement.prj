import pandas as pd
from sales.models import Shift
from inventory.models import Inventory
from setup.models import Branch, Product, Staff, Pump

print('Importing data......')

shift = pd.read_csv('sales/shift.csv')
print(f'\n{shift.head()}')
print('\nData imported...')
for index, row in shift.iterrows():
	print(f'Index {index} - Row {row}')
	shift, created = Shift.objects.get_or_create(
    type = row['type'],
    start = row['start'],
    end = row['end'],
    staff = Staff.objects.get(id =row['staff_id']),
    is_active= row['is_active'],
    pump = Pump.objects.get(id = row['pump_id']),
    stock = row['stock'],
    branch = Branch.objects.get(id = row['branch_id']),
    product =  Product.objects.get(id = row['product_id']),
    inventory = None
    )

	shift.save()
print('\nData has been loaded into the database')

print('\nUpdating shift with Inventory records')
for shift in Shift.objects.all():
    if shift.branch_id and shift.product_id and shift.stock:
        # Find matching inventory instance
        try:
            inventory = Inventory.objects.get(branch_id=shift.branch_id, product_id=shift.product_id, quantity=shift.stock)
            print(inventory)
            shift.inventory = inventory
            shift.save()
        except Inventory.DoesNotExist:
            print("Inventory is empty")

print('\nAll shifts updated successfully')

