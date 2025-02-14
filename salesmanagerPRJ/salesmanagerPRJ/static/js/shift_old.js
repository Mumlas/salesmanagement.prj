document.addEventListener('DOMContentLoaded', function() {
    // Branch event listener
    document.getElementById('branchIDField').addEventListener('click', function() {
      var branchId = document.getElementById('branchIDField').value;
      console.log(branchId);
      
      // Make an AJAX request to fetch the staff based on the selected branch
      fetch(`get-staff/${branchId}/`)
        .then(response => response.json())
        .then(data => {
          var staffSelect = document.getElementById('staff');
          staffSelect.innerHTML = '';  // Clear existing options
          var defaultOption = document.createElement('option');
          defaultOption.value = '';
          defaultOption.textContent = 'Select pump attendant';
          staffSelect.appendChild(defaultOption);  // Add default placeholder option

          // Populate facility options based on the fetched data
          data.forEach(staff => {
            var option = document.createElement('option');
            option.value = staff.id;
            option.textContent = staff.name;
            staffSelect.appendChild(option);
          });
        });


      // Make an AJAX request to fetch the facilities based on the selected branch
      fetch(`get-facilities/${branchId}/`)
        .then(response => response.json())
        .then(data => {
          var facilitySelect = document.getElementById('facility');
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

      // Facility event listener
      document.getElementById('facility').addEventListener('change', function() {
        var facilityId=document.getElementById('facility').value;
        // Make an AJAX request to fetch the facilities based on the selected branch
        fetch(`get-pumps/${facilityId}/`)
          .then(response => response.json())
          .then(data => {
            var pumpSelect = document.getElementById('pump');
            pumpSelect.innerHTML = '';  // Clear existing options
            var defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select a pump';
            pumpSelect.appendChild(defaultOption);  // Add default placeholder option
            // Populate facility options based on the fetched data
            data.forEach(pump => {
              var option = document.createElement('option');
              option.value = pump.id;
              option.textContent = pump.name;
              pumpSelect.appendChild(option);
            });
          });
      
    // Facility event listener
      var branchId=document.getElementById('branchIDField').value;
      var facilityId=document.getElementById('facility').value;
      console.log("facility id", facilityId);
      console.log("branch id", branchId);
      // Make an AJAX request to fetch the facilities based on the selected branch
      fetch(`get-products/${facilityId}/${branchId}/`)
        .then(response => response.json())
        .then(data => {
        // Add default placeholder option
          console.log("Data",data);
          // Populate facility options based on the fetched data
          document.getElementById('product').value = data.product_name;
          document.getElementById('stock').value = data.inStock
        });
      });
  });
});