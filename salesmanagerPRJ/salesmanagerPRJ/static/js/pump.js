document.addEventListener('DOMContentLoaded', function() {
    // Branch event listener
    document.getElementById('branchIDField').addEventListener('change', function() {
      var branchId = this.value;
      
      // Make an AJAX request to fetch the facilities based on the selected branch
      fetch(`get-facilities/${branchId}/`)
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
    });

});