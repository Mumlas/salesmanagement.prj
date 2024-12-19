/*$(document).ready(function () {
    const productName = $('#product').val();
    $('#quantitySold').keyup(function () {
        const quantity = $(this).val();

        if (quantity) {
            // ajax call
            $.ajax({
                url: 'get-price/',
                method: 'GET',
                data: {
                    product_name : productName,
                    quantity: quantity,
                },
                success: function (response) {
                    const price = response.price;
                    const actualSales = $('#actualSales').val();

                    $('#expected_sales').val( price * quantity);
                    const expectedSales = $('#expectedSales').val();

                    $('#margin').val(expectedSales-actualSales);
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching data:', error)
                }
            });
        } else {
            // clear input
            $('#quantitySOld').val(0);
            $('#actualSales').val(0);
            $('#margin').val(0)
        }
    });
});
*/
document.addEventListener('DOMContentLoaded', function (){
    productName = document.getElementById('product').value;
    console.log('Product', productName);

    fetch(`get-price/${productName}/`)
    .then(response => response.json() )
    .then(data => {
        let prices = data
        console.log('Response', prices);
        price = parseFloat(prices.name);
        console.log('Price:', data['name']);
        document.getElementById('quantitySold').addEventListener("keyup", function () {
            quantity = parseFloat(document.getElementById('quantitySold').value);
            console.log('Quantity:', quantity);
            document.getElementById('expectedSales').value = price * quantity;
            document.getElementById('margin').value = 0- document.getElementById('expectedSales').value;
        });
    });

    document.getElementById('actualSales').addEventListener("keyup", function () {
        actualSales = document.getElementById('actualSales').value;
        document.getElementById('margin').value = actualSales - document.getElementById('expectedSales').value;
    });
});