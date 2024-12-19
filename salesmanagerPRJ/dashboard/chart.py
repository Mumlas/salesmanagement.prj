from inventory.models import Inventory
from django.shortcuts import render
import plotly.graph_objects as go
from django.db.models import Sum, F
from plotly.offline import plot
from sales.models import Sales
import plotly.express as px
import pandas as pd
import numpy as np


def plot_barchart(request,staff, inventory, sales):

    staff_id = request.user.staff.id

    branch_id = staff.objects.values_list('branch_id', flat=True).get(id=staff_id)
    stock = inventory.filter(branch_id=branch_id).values('product_name','quantity') #.annotate(quantity_available = Sum('quantity'))
    sales_data = sales.filter(shift__inventory__branch=branch_id).values('product_name').annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'))
    sales_date = sales.filter(shift__inventory__branch=branch_id).values('product_name', date=F('shift__end')).annotate(quantity_sold =Sum('quantity_sold'),actual_sales = Sum('actual_sales'), expected_sales=Sum('expected_sales'))    
   
    dates = [e['date'] for e in sales_date]
    actual_sdate = [e['actual_sales'] for e in sales_date]
    expected_sdate = [e['expected_sales'] for e in sales_date]
    quantity_sdate = [qs['quantity_sold'] for qs in sales_date]
    product_sdate = [p['product_name'] for p in sales_date]

    actual = [e['actual_sales'] for e in sales_data] or 0
    expected = [e['expected_sales'] for e in sales_data] or 0
    product = [p['product_name'] for p in stock] or None
    quantity_available = [qa['quantity'] for qa in stock] or 0
    quantity_sold = [qs['quantity_sold'] for qs in sales_data] or 0
    product_stock = [ps['product_name'] for ps in stock] or 0

    print(f'Products: {product}')
    print(f'Actuals: {actual}')
    print(f'Expected: {expected}')
    print(f'Quantity Available: {quantity_available}')
    print(f'Dates: { dates}')
    
    sales_df = pd.DataFrame({'Product' : product, 'Actual': actual, 'Expected':expected, 'QuantitySold':quantity_sold, 'Stock':quantity_available})
    date_df = pd.DataFrame({'Product' : product_sdate, 'Date':dates, 'Actual': actual_sdate, 'Expected':expected_sdate, 'QuantitySold':quantity_sdate})
    stock_df = pd.DataFrame({'Product':product_stock, 'Stock':quantity_available})
    
    date_df['Date'] = pd.Series(date_df['Date']).sort_index()
    print(date_df)

    date_df.index = pd.DatetimeIndex(date_df.Date)
    print(date_df)

    fig_sales0 = px.bar(sales_df, x='Product', y= 'Actual')
    fig_stock = px.bar(stock_df, x='Product', y= "Stock")
    #fig_line = px.line(date_df, x='Date', y= 'Actual', color='Product')

    print(date_df)

    actual = go.Bar(
        x= sales_df['Product'],
        y = sales_df['Actual'],
        name='Actual Sales',
        text = sales_df['Actual']
    )

    expected = go.Bar(
        x= sales_df['Product'],
        y = sales_df['Expected'],
        name='Expected Sales',
        text = sales_df['Expected']
    )

    fig_data = [actual, expected]
    layout = go.Layout(barmode='group', legend=dict(yanchor="middle", xanchor="center", x=0.4, orientation="h"))

    ago_dt = go.Scatter(
        x= date_df['Date'].astype(dtype=str), #pd.to_datetime(date_df.index),
        y = date_df[date_df['Product']=="AGO"]['Actual'],
        name='AGO - Sales',
    )

    pms_dt = go.Scatter(
        x= date_df['Date'].astype(dtype=str), #pd.to_datetime(date_df.index).strftime("%Y-%m-%d"),
        y = date_df[date_df['Product']=="PMS"]['Actual'],
        name='PMS - Sales',
        #marker_color='orange'
    )


    fig_date = [ago_dt, pms_dt]
    
    fig_sales = go.Figure(data=fig_data, layout=layout)
    fig_line = go.Figure(data=fig_date)

    """fig_sale = go.Figure(
        layout=go.Layout(
            height=450, width=700, barmode="group", yaxis_showticklabels=False, yaxis_showgrid=False,
            yaxis2=go.layout.YAxis(
                visible=False, matches="y", overlaying="y",anchor="x",
            ),
            font=dict(size=24), legend_x=0, legend_y=1, legend_orientation="h", margin=dict(b=0,t=10,l=0,r=10)
        )
    )

    colors = {
        "AGO": {
            "Actual":"#F28F10",
            "Expected":"#F6C619",
            "Stock":"#FADD75",
        },
        "PMS": {
            "Actual":"#286045",
            "Expected":"#5EB88A",
            "Stock":"#9ED4B9",            
        }
    }

    for i, t in enumerate(colors):
        for j, col in enumerate(df1[t].columns):
            if (df1[t][col] == 0).all():
                continue
            fig_sale.add_bar(
            x = df1.index,
            y=df1[t][col],
            yaxis=f"y{i + 1}",
            offsetgroup=str(i),
            width=1/2,
            legendgroup=t,
            legendgrouptitle_text=t,
            name=col,
            marker_color=colors[t][col],
            marker_line=dict(width=2, color="#333"),
            hovertemplate="%{y}<extra></extra>"

    )"""
    #for f in [fig_sales, fig_stock, fig_line]:
    #    f.update_yaxes(autorange="reversed")

    return [fig_sales, fig_stock, fig_line]

def md_chart(sales_df, date_df, stock_df):

    fig_stock = px.bar(stock_df, x='Product', y= "Stock")

    actual = go.Bar(
        x= sales_df['Product'],
        y = sales_df['Actual'],
        name='Actual Sales',
        text = sales_df['Actual']
    )

    expected = go.Bar(
        x= sales_df['Product'],
        y = sales_df['Expected'],
        name='Expected Sales',
        text = sales_df['Expected']
    )

    fig_data = [actual, expected]
    layout = go.Layout(barmode='group', legend=dict(yanchor="middle", xanchor="center", x=0.4, orientation="h"))

    ago_dt = go.Scatter(
        x= date_df['Date'].astype(dtype=str), #pd.to_datetime(date_df.index),
        y = date_df[date_df['Product']=="AGO"]['Actual'],
        name='AGO - Sales',
    )

    pms_dt = go.Scatter(
        x= date_df['Date'].astype(dtype=str), #pd.to_datetime(date_df.index).strftime("%Y-%m-%d"),
        y = date_df[date_df['Product']=="PMS"]['Actual'],
        name='PMS - Sales',
        #marker_color='orange'
    )


    fig_date = [ago_dt, pms_dt]
    
    fig_sales = go.Figure(data=fig_data, layout=layout)
    fig_line = go.Figure(data=fig_date)

    fig_line.update_layout({"title":'Sales History by Products',
                            "xaxis":{"title":'Period (Daily)'},
                            "yaxis":{"title":'Amount (millions)'}})

    return [fig_sales, fig_stock, fig_line]


def get_data_summary(request):

    # query the relevant models
    # 1. inventory
    inventory = ""
    querysets = ""
    columns = [col[0] for col in querysets]
    data = [dict(zip(columns, row)) for row in querysets]

    # convert to dataframe

    df = pd.DataFrame(data)
    # get the data into a list

    tile_data = []
    
    for index, row in df.iterrows():
        tile_data.append({
            'Data':row['Data'],
            'Metric': row['Mteric']
        })
    
    context = {tile_data}

    return context

def get_data_chart(request, qs):

    role = request.user.role

    # query the relevant models
    inventory = qs.objects.all().select_related('product')

    # convert to dataframe
    data_inventory = [
        {
            'product':x.product.productName,
            'quantity':x.quantity
        } for x in inventory
    ]

    # get the columns from the dataframe

    # convert the dataframe to a dictionary for passing to the template
    df_inventory = pd.DataFrame(data_inventory)

    fig = px.bar(
        df_inventory, x= 'product', y='quantity', color='product'
    )

    fig.update_yaxes(autorange="reversed")
    gantt_plot = plot(fig, output_type="div")
    context = {'plot_div': gantt_plot}


    return context

def chart_view(request, qs):
    staff_id = request.user.staff.id
    branch_id = qs.objects.values_list('branch_id', flat=True).get(id=staff_id)
    inventory = qs.objects.filter(branch_id=branch_id)
    branches = qs.objects.get(id=branch_id)
    shifts = qs.objects.filter().select_related('inventory')
    sales = qs.objects.filter().select_related('shift')

    print(sales)

    sales_date = go.Figure(data=[go.Bar(
        x =[s.shift.start for s in sales],
        y =[s.actual_sales for s in sales],
        textposition = 'auto',
    )])

    sales_poducts = go.Figure(data=[go.Bar(
        x =[s.shift.inventory.product.productName for s in sales],
        y =[s.actual_sales for s in sales],
        textposition = 'auto',
    )])

    sales_date_plot:str = plot(sales_date, output_type='div')
    sales_product_plot:str = plot(sales_poducts, output_type='div')

    context = {'sales_product_plot': sales_product_plot,
               'sales_date_plot':sales_date_plot}
    return render(request, 'dashboard/supervisor/supervisor_main.html' , context)

def manager_chart_data(request, qs):

    staff_id = request.user.staff.id
    branch_id = qs.objects.values_list('branch_id', flat=True).get(id=staff_id)
    inventory = qs.objects.filter(branch_id=branch_id).select_related('product').values('quantity','product__productName')
    sales_data = qs.objects.filter(shift__inventory__branch=branch_id) .select_related('shift').values('actual_sales','expected_sales', 'shift__start')
    
    dates = [e['shift__start'].strftime('%Y-%m-%d') for e in sales_data]
    actual = [e['actual_sales'] for e in sales_data]
    expected = [e['expected_sales'] for e in sales_data]
    product = [p['product__productName'] for p in inventory]
    quantity = [p['quantity'] for p in inventory]

    context = {
        'dates':dates,
        'actual':actual,
        'expected':expected,
        'product':product,
        'quantity':quantity,
    }
    print(f'Context:\n {context}')
    return context
    
    

