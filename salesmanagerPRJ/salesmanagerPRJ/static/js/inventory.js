document.addEventListener('DOMContentLoaded', function(){
  document,getElementById("branchIDField").addEventListener('change', function(){
    var branchId=this.value;
    console.log('testing');

    fetch(`get-facilities/${branchId}/`)
    .then(response => response.json())
    .then(data => {
      var facilitySelect = document.getElementById('facilityIDField');
      facilitySelect.innerHTML = ''; // clear options
      var defaultOption=document.createElement('option');
      defaultOption.value='';
      defaultOption.textContent= 'select tank';
      facilitySelect.appendChild(defaultOption); // add default option

      data.forEach(facility => {
        var option=document.createElement(option);
        option.value = facility.id;
        option.textContent=facility.name;
        facilitySelect.appendChild(option);
      });
    });
  });

  // Facility event listener
  document.getElementById('facilityIDField').addEventListener('change', function(){
    var branchId=document.getElementById('branchIDField').value;
    var facilityId=document.getElementById('facilityIDField').value;

    console.log(branchId);
    console.log(facilityId);

    if (branchId && facilityId) {
      fetch(`get-products/14/1/`)
      .then(response=> response.json())
      .then(data => {
        document.getElementById('productIDField').value = data.product_name;
        document.getElementById('quantityinSTock').value = data.inStock;
      })
      .catch(error => console.log('Error', error));
    } else {
      console.error('Branch or Storage Tank is missing');
    }
  });
});


/*
document.addEventListener('DOMContentLoaded', function() {
    // Branch event listener
    document.getElementById('branchIDField').addEventListener('change', function() {
      var branchId = this.value;
      
      // Make an AJAX request to fetch the facilities based on the selected branch
      fetch(`get-facilities/${branchId}/`)
      console.log('testing..')
        .then(response => response.json())
        .then(data => {
          var facilitySelect = document.getElementById('facilityIDField');
          facilitySelect.innerHTML = '';  // Clear existing options
          var defaultOption = document.createElement('option');
          defaultOption.value = '';
          defaultOption.textContent = 'Select a facility';
          facilitySelect.appendChild(defaultOption);  // Add default placeholder option
          
          // Populate facility options based on the fetched data
          data.forEach(facility => {
            var option = document.createElement('option');
            option.value = facility.id;
            option.textContent = facility.name;
            facilitySelect.appendChild(option);
          });
        });
        console.log(data);
    });
 
    // Facility event listener
    document.getElementById('facilityIDField').addEventListener('change', function() {
      const branchId = document.getElementById("branchIDField").value;
      const facilityId = document.getElementById("facilityIDField").value;

      console.log(branchId);
      // Make an AJAX request to fetch the products based on the selected facility

      if (branch && facility) {
        fetch(`get-products/${branchId}/${facilityId}/`)
        .then(response => response.json())
        .then(data => {
          // Populate the quantity field with the fetched quantity quanityinStock
          document.getElementById('productIDField').value = data.product_name;
          document.getElementById('quantityinStock').value = data.inStock;
        })
        .catch(error=> console.log("Error",error));
      } else {
        console.error("Branch or facility is missing");
      }

        });
    });
  
    // Product event listener
    document.getElementById('productIDField').addEventListener('change', function() {
      var productId = this.value;
      
      // Make an AJAX request to fetch the current quantity in stock
      fetch(`get-quantity/${productId}/`)
        .then(response => response.json())
        .then(data => {
          // Populate the quantity field with the fetched quantity
          document.getElementById('quantityField').value = data.quantity;
        });
    });
  */