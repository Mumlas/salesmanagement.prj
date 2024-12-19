
$(document).ready(function () {
    // function to update the charts
    function updateDashboard() {
        // filters
        const start_date = $('#startdateFilter').val();
        const end_date = $('#enddateFilter').val();
        const branch = $('#branchFilter').val();
        const product = $('#productFilter').val();
        console.log('Start Date', start_date);
        console.log('End Date', end_date);
        console.log('Branch', branch);
        console.log('Product', product);

        //send ajax request with the filtered data
        $.ajax({
            url: "{% url 'md_ajax_data' %}",
            data: {
                start_date: start_date,
                end_date: end_date,
                branch: branch,
                produc: product,
            },
            success: function (response) {
                // update the dashboard visuals
                $('#sales_history').html(response.sales_history);
                $('#stock_chart').html(response.stock_chart);
                $('#branch_chart').html(response.branch_chart);

                // KPIs
                $('aggegrate_sales').text(response.aggegrate_sales);
                $('aggregate_stock').text(response.aggregate_stock);

                //table
                const sales_table = $('#sales_table');
                sales_table.empty(); //clear existing table
                response.sales_table.forEach(row => {
                    const newRow = `<tr> 
                    <td>${ row.branch }</td>
                    <td>${ row.storage.storageDesc }</td>
                    <td>${ product.productName }</td>
                    <td>${ quantity }</td>
                    <td>${ dateUpdated }</td>
                    <td>${ updatedBy }</td>
                    </tr>`;
                    sales_table.append(newRow);
                });

                const stock_table = $('#stock_table');
                const shift_table = $('#shift_table');

            },
            error: function () {
                alert('Failed to load data. Please try again');
            }
        });
    }

    // Event listener
    let debounceTimer;
    function debounce(func, delay) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(func, delay);
    }

    //using debouns in the eventlistener
    $('#start-date, #end-date, #branch, #product').on('change', function () {
        debounce(updateDashboard, delay=300); //300ms delay
    });
});
