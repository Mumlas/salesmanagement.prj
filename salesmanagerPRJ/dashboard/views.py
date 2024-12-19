from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import numpy as np
from setup.models import Staff, Branch, Storage, Price, Product
from sales.models import Sales, Shift
from inventory.models import Inventory
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Max
from django.db.models.functions import TruncDate
import pandas as pd
from django.contrib import messages
from annoying.functions import get_object_or_None
from dashboard.chart import plot_barchart, md_chart
import plotly.graph_objects as go
import plotly.express as px



def count_object(model, *args, **kwargs):
    pass

@login_required
def md_chart(request):

    if request.method == "POST":

        # filter by date
        start_date = request.POST.get('startdateFilter')
        end_date = request.POST.get('enddateFilter')
        branch_id = request.POST.get('branchFilter')
        product_id = request.POST.get('productFilter')


        print(f'Start: {start_date}')
        print(f'End: {end_date}')
        print(f'Branch: {branch_id}')
        print(f'Product: {product_id}')

        #base queryset
        sales = Sales.objects.all().select_related()
        stocks = Inventory.objects.all().select_related()
        shifts = Shift.objects.filter(status='On-Going').select_related()
        branches = Branch.objects.all()
        products = Product.objects.all()

        if start_date and end_date:
            # sales by date
            sales = sales.filter(shift__end__range=[start_date, end_date])
            stocks = stocks.filter(dateUpdated__range = [start_date, end_date])

        if branch_id:
            sales = sales.filter(shift__inventory__branch_id=branch_id) #.select_related().values(product_name = F('shift__inventory__product__productName')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'))
            stocks = stocks.filter(branch_id=branch_id) #.select_related('product').values(product_name = F('product__productName')).annotate(quantity = Sum('quantity')).order_by('quantity')

        if product_id:
            sales = sales.filter(shift__inventory__product_id=product_id) #.select_related().values(product_name = F('shift__inventory__product__productName')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'))
            stocks = stocks.filter(product_id=product_id) #.select_related('product').values(product_name = F('product__productName')).annotate(quantity = Sum('quantity')).order_by('quantity')
    
        aggregate_sales = sales.select_related().values(product_name = F('shift__inventory__product__productName')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))
        aggregate_stock = stocks.select_related().values(product_name = F('product__productName')).annotate(quantity = Sum('quantity')).order_by('quantity')
        aggregate_sales_date = sales.select_related().values(product_name = F('shift__inventory__product__productName'), dates=TruncDate('shift__end')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'))    
        aggregate_stock_date = stocks.select_related().values(product_name = F('product__productName'), dates=TruncDate('dateUpdated')).annotate(quantity =Sum('quantity'))  
        sales_branch = sales.select_related().values(branch = F('shift__inventory__branch__branchName'), product_name = F('shift__inventory__product__productName')).annotate(quantity_sold =Sum('quantity_sold'), actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))
        branch_performance = sales.select_related().values(branch = F('shift__inventory__branch__branchName')).annotate(quantity_sold =Sum('quantity_sold'), actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))

        sales_date = [item['dates'] for item in aggregate_sales_date]
        stock_date = [item['dates'] for item in aggregate_stock_date]

        sales_actual = [item['actual_sales'] for item in aggregate_sales]
        sales_expected = [item['expected_sales'] for item in aggregate_sales]        
        stock_qtty = [item['quantity'] for item in aggregate_stock]

        sales_product = [item['product_name'] for item in aggregate_sales]
        stock_product = [item['product_name'] for item in aggregate_stock]
        sale_branch = [item['actual_sales'] for item in branch_performance]
        branch = [item['branch'] for item in branch_performance]

        sales_df = pd.DataFrame.from_records(aggregate_sales_date)
        print(sales_df)
        sales_history = go.Figure(
            data = [go.Scatter(x=sales_date, y= sales_actual)],
            layout = go.Layout(title='Sales History', xaxis=dict(title='Date'), yaxis=dict(title='Actual Sales'))
        )

        stock_chart = go.Figure(
            data=[go.Bar(x=stock_product, y=stock_qtty)],
            layout = go.Layout(title='Status of Stock', xaxis=dict(title='Product'), yaxis=dict(title='Quantity'))
        )

        branch_chart = go.Figure(
            data=[go.Bar(x=branch, y=sale_branch)],
            layout = go.Layout(title='Sales by Branches', xaxis=dict(title='Branches'), yaxis=dict(title='Actual Sales'))
        )

        context = {
            'aggregate_stock_date':aggregate_stock_date,
            'aggregate_sales_date':aggregate_sales_date,
            'aggregate_stock':aggregate_stock,
            'aggregate_sales':aggregate_sales,
            'sales_date':sales_date,
            'stock_date':stock_date,
            'sales_actual':sales_actual,
            'sales_expected':sales_expected,
            'stock_qtty':stock_qtty,
            'sales_product':sales_product,
            'stock_product':stock_product,
            'branches':branches,
            'products':products,
            'stocks':stocks,
            'sales':sales,
            'shifts':shifts,
            'sales_branch':sales_branch,
            'sales_history':sales_history.to_html(full_html=False),
            'stock_chart':stock_chart.to_html(full_html=False),
            'branch_chart':branch_chart.to_html(full_html=False),
        }

        return render(request, 'dashboard/md/md_main.html' ,context)

@login_required
def accountant_view(request):

    staff_id = request.user.staff.id
    branch_id = Staff.objects.values_list('branch_id', flat=True).get(id=staff_id)
    inventory = Inventory.objects.filter(branch_id=branch_id)
    branches = Branch.objects.get(id=branch_id)
    shifts = Shift.objects.filter().select_related('inventory')
    sales = Sales.objects.filter(shift__inventory__branch = branch_id).select_related('shift')

    context = {
        'sales':sales,
        'shifts':shifts,
        'branches':branches
    }

    return context

@login_required
def attendant_view(request):

    staff_id = request.user.staff.id
    staff = Staff.objects.get(id=staff_id)
    shifts = Shift.objects.filter(staff_id=staff_id).select_related('inventory')
    q_sold = Sales.objects.filter(shift__staff=staff_id).select_related('shift').values(product_name=F('shift__inventory__product__productName')).annotate(quantity=Sum('quantity_sold'))
    v_sold = Sales.objects.filter(shift__staff=staff_id).select_related('shift').values(product_name=F('shift__inventory__product__productName')).annotate(value=Sum('actual_sales'))
    #stock = Inventory.objects.filter(shift__staff=staff_id).select_related('product').values(product_name = F('product__productName')).annotate(quantity = Sum('quantity')).order_by('quantity')
    max_sales = Sales.objects.filter(shift__staff=staff_id).select_related('shift').values(date=F('shift__end')).annotate(value=Max('actual_sales')).order_by('-value')[:1]
    #inventory_count = Inventory.objects.filter(shift__staff=staff_id).count()
    sales_count = Sales.objects.filter(shift__staff = staff_id).count()
    sales = Sales.objects.filter(shift__staff = staff_id).select_related('shift')
    next_shift = Shift.objects.filter(staff_id=staff_id, status='Pending').order_by('start').first()#[:0]
    completed_shift = Shift.objects.filter(staff_id=staff_id, status='Ended').count()
    shift_count = Shift.objects.filter(staff_id=staff_id).count()

    print(f'Sales count: {sales_count}')
    print(f'Sales {sales}')
    print(f'Quantity sold: {q_sold}')
    print(f'Sales Value: {v_sold}')
    print(f'Max sales {max_sales}')
    print(f'Next Shift: {next_shift}')

    #for chart
    branch = request.user.staff.branch
    
    context = {
        'branch':branch,
        'shifts':shifts,
        'sales':sales,
        'q_sold':q_sold,
        'v_sold':v_sold,
        'max_sales':max_sales,
        'sales_count':sales_count,
        'next_shift':next_shift,
        'shift_count':shift_count,
        'completed_shift':completed_shift,
    }
    
    return context

@login_required
def manager_view(request):    
    
    branch_id = request.user.staff.branch_id
    branch = Branch.objects.get(id=branch_id)
    inventories = Inventory.objects.filter(branch_id=branch_id).select_related()
    shifts = Shift.objects.filter(inventory__branch=branch_id).select_related('inventory')
    staff = Staff.objects.filter(branch_id=branch)
    storages = Storage.objects.filter(branch_id=branch_id)
    prices = Price.objects.all()
    q_sold = Sales.objects.filter(shift__inventory__branch=branch_id).select_related('shift').values(product_name=F('shift__inventory__product__productName')).annotate(quantity=Sum('quantity_sold'))
    v_sold = Sales.objects.filter(shift__inventory__branch=branch_id).select_related('shift').values(product_name=F('shift__inventory__product__productName')).annotate(value=Sum('actual_sales'))
    stock = Inventory.objects.filter(branch_id=branch).select_related('product').values(product_name = F('product__productName')).annotate(quantity = Sum('quantity')).order_by('quantity')
    max_sales = Sales.objects.filter(shift__inventory__branch=branch_id).select_related('shift').values(date=F('shift__end')).annotate(value=Max('actual_sales')).order_by('-value')[:1]
    inventory_count = Inventory.objects.filter(branch_id=branch_id).count()
    sales_count = Sales.objects.filter(shift__inventory__branch = branch_id).count()
    sales = Sales.objects.filter(shift__inventory__branch = branch_id).select_related()

    #chart
    chart_list = plot_barchart(request, Staff, stock, v_sold)
    print(f'Pending Shifts: {shifts.filter(status="Pending")}')
    context = {
        'shifts':shifts,
        'inventories':inventories,
        'staff':staff,
        'branch':branch,
        'storages':storages,
        'prices':prices,
        'stock':stock,
        'q_sold':q_sold,
        'v_sold':v_sold,
        'max_sales':max_sales,
        'inventory_count':inventory_count,
        'sales_count':sales_count,
        'sales':sales,
        'fig_sales':chart_list[0].to_html(),
        'fig_stock':chart_list[1].to_html(),
        'fig_line':chart_list[2].to_html(),
    }

    return context

@login_required
def md_view(request):
    
    #base queryset
    branches = Branch.objects.all()
    products = Product.objects.all()
    sales = Sales.objects.all().select_related()
    stocks = Inventory.objects.all().select_related()
    shifts = Shift.objects.filter(status='On-Going').select_related()

    #aggegrate summary
    aggregate_sales = sales.select_related().values(product_name = F('shift__inventory__product__productName')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))
    aggregate_stock = stocks.select_related().values(product_name = F('product__productName')).annotate(quantity = Sum('quantity')).order_by('quantity')
    aggregate_sales_date = sales.select_related().values(product_name = F('shift__inventory__product__productName'), dates=TruncDate('shift__end')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))    
    aggregate_stock_date = stocks.select_related().values(product_name = F('product__productName'), dates=TruncDate('dateUpdated')).annotate(quantity =Sum('quantity'))  
    sales_branch = sales.select_related().values(branch = F('shift__inventory__branch__branchName'), product_name = F('shift__inventory__product__productName')).annotate(quantity_sold =Sum('quantity_sold'), actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))
    branch_performance = sales.select_related().values(branch = F('shift__inventory__branch__branchName')).annotate(quantity_sold =Sum('quantity_sold'), actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'), margin=Sum('margin'))
    
    
    sales_df = pd.DataFrame.from_records(aggregate_sales_date)

    print(f'Sales: { sales_df }')
    sales_date = [item['dates'] for item in aggregate_sales_date]
    stock_date = [item['dates'] for item in aggregate_stock_date]

    sales_actual = [item['actual_sales'] for item in aggregate_sales]
    sales_expected = [item['expected_sales'] for item in aggregate_sales]        
    stock_qtty = [item['quantity'] for item in aggregate_stock]

    sales_product = [item['product_name'] for item in aggregate_sales]
    stock_product = [item['product_name'] for item in aggregate_stock]
    sale_branch = [item['actual_sales'] for item in branch_performance]
    branch = [item['branch'] for item in branch_performance]

    sale_history = go.Figure(
        data = [go.Scatter(x=sales_date, y= sales_actual)],
        layout = go.Layout(title='Sales History', xaxis=dict(title='Date'), yaxis=dict(title='Actual Sales'))
    )

    sale_history.add_trace(go.Scatter(x=sales_date, y=sales_expected))

    sales_history = px.line(sales_df, x='dates', y= 'actual_sales', color='product_name', 
                            color_discrete_sequence=['navy', 'darkorange','green','red','brown'], title='Sales History',
                            hover_name='actual_sales', hover_data={'product_name':True, 'margin':True},
                            labels={'actual_sales':'Sales Amount', 'date':'Date'}, template='plotly_white')

    stock_chart = go.Figure(
        data=[go.Bar(x=stock_product, y=stock_qtty)],
        layout = go.Layout(title='Status of Stock', xaxis=dict(title='Product'), yaxis=dict(title='Quantity'))
    )

    branch_chart = go.Figure(
        data=[go.Bar(x=branch, y=sale_branch)],
        layout = go.Layout(title='Sales by Branches', xaxis=dict(title='Branches'), yaxis=dict(title='Actual Sales'))
    )

    context = {
        'aggregate_stock_date':aggregate_stock_date,
        'aggregate_sales_date':aggregate_sales_date,
        'aggregate_stock':aggregate_stock,
        'aggregate_sales':aggregate_sales,
        'sales_date':sales_date,
        'stock_date':stock_date,
        'sales_actual':sales_actual,
        'sales_expected':sales_expected,
        'stock_qtty':stock_qtty,
        'sales_product':sales_product,
        'stock_product':stock_product,
        'branches':branches,
        'products':products,
        'stocks':stocks,
        'sales':sales,
        'shifts':shifts,
        'sales_branch':sales_branch,
        'sales_history':sales_history.to_html(full_html=False),
        'stock_chart':stock_chart.to_html(full_html=False),
        'branch_chart':branch_chart.to_html(full_html=False),
    }

    return context

@login_required
def supervisor_view(request):
    
    branch = request.user.staff.branch_id
    shifts =Shift.objects.filter().select_related('inventory')
    sales = Sales.objects.filter().select_related('shift')
    inventories = Inventory.objects.filter(branch_id=branch)
    staff = Staff.objects.filter(branch_id=branch)
    storages = Storage.objects.filter(branch_id=branch)

    context = {
        'shifts':shifts,
        'sales':sales,
        'inventories':inventories,
        'staff':staff,
        'storages':storages,
    }
    
    return context

@login_required
def main_view(request):
    role = request.user.role
    
    match role:
        
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/supervisor/supervisor_main.html', context)
        
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/manager/manager_main.html', context)
        
        case 'cashier_accountant':
            context = accountant_view(request)
            return render(request, 'dashboard/accountant/accountant_main.html', context)
        
        case 'md_ceo':
            context = md_view(request)
            return render(request, 'dashboard/md/md_main.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/attendant/attendant_main.html', context)

@login_required
def branch_view(request):
    
    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/branch.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/branch.html', context)
        case 'cashier_accountant':
            context = accountant_view(request)
            return render(request, 'dashboard/branch.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/branch.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/branch.html', context)

@login_required
def product_view(request):
    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/product.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/product.html', context)
        case 'cashier_accountant':
            context = accountant_view(request)
            return render(request, 'dashboard/product.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/product.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/product.html', context)

@login_required
def shift_view(request):

    role = request.user.role
    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/supervisor/supervisor_shift.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/manager/manager_shift.html', context)
        case 'cashier_accountant':
            context = accountant_view(request)
            return render(request, 'dashboard/accountan/accountant_shift.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/md/md_shift.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/attendant/attendant_shift.html', context)

@login_required
def sale_view(request):
    role = request.user.role

    match role:
        case 'supervisor':
            context = supervisor_view(request)
            return render(request, 'dashboard/supervisor/supervisor_sales.html', context)
        case 'manager':
            context = manager_view(request)
            return render(request, 'dashboard/manager/manager_sales.html', context)
        case 'cashier_accountant':
            context = accountant_view(request)
            return render(request, 'dashboard/accountant/accountant_sales.html', context)
        case 'md':
            context = md_view(request)
            return render(request, 'dashboard/md/sales.html', context)

        case _:
            context = attendant_view(request)
            return render(request,'dashboard/attendant/attendant_sales.html', context)

