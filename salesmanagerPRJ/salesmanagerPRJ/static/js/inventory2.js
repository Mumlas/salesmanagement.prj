document.addEventListener('DOMContentLoaded', function(){
  document.getElementById("branchIDField").addEventListener('change', function(){
    var branchId=this.value;

    fetch(`get-facilities/${branchId}/`)
    .then(response => response.json())
    .then(data => {
      var facilitySelect = document.getElementById('facilityIDField');
      facilitySelect.innerHTML = ''; // clear options
      var defaultOption=document.createElement('option');
      defaultOption.value='';
      defaultOption.textContent= 'select tank';
      facilitySelect.appendChild(defaultOption); // add default option
      console.log(data);
    
      data.forEach(facility => {
        var option=document.createElement('option');
        option.value = facility.id;
        option.textContent=facility.name;
        facilitySelect.appendChild(option);
        console.log(facility);
      });

    });

  });

  // Facility event listener
  document.getElementById('facilityIDField').addEventListener('change', function(){
    var branchId=document.getElementById('branchIDField').value;
    var facilityId=document.getElementById('facilityIDField').value;

    if (branchId && facilityId) {
        console.log(branchId);
        console.log(facilityId);
      fetch(`get-products/${facilityId}/${branchId}/`)
      .then(response=> response.json())
      .then(data => {
        document.getElementById('productIDField').value = data.product_name;
        document.getElementById('quantityinStock').value = data.inStock;
      })
      .catch(error => console.error('Error', error));
    } else {
      console.error('Branch or Storage Tank is missing');
    }
  });
});