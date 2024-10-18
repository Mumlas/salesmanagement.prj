document.getElementById('branch').addEventListener('change', function() {
    var branchId = this.value;
    
    fetch(`/get-facilities/${branchid}`)
      .then(response => response.json())
      .then(data => {
        var facilitySelect = document.getElementById('facility');
        facilitySelect.innerHTML = '';  // Clear the current options
        data.forEach(facility => {
          var option = document.createElement('option');
          option.value = facility.id;
          option.textContent = facility.name;
          facilitySelect.appendChild(option);
        });
      });
  });
  
  document.getElementById('facility').addEventListener('change', function() {
    var facilityId = this.value;
    
    fetch(`/get-products/${facilityId}`)
      .then(response => response.json())
      .then(data => {
        var productSelect = document.getElementById('product');
        productSelect.innerHTML = '';  // Clear current options
        data.forEach(product => {
          var option = document.createElement('option');
          option.value = product.id;
          option.textContent = product.name;
          productSelect.appendChild(option);
        });
      });
  });
  
  document.getElementById('product').addEventListener('change', function() {
    var productId = this.value;
    
    fetch(`/get-quantity/${productId}`)
      .then(response => response.json())
      .then(data => {
        document.getElementById('quantity').value = data.quantity;
      });
  });
  