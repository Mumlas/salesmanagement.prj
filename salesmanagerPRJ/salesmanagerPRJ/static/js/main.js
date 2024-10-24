document.addEventListener('DOMContentLoaded', function() {
    // Populate branches dropdown
    fetch('get-branches/')
      .then(response => response.json())
      .then(data => {
        let branchSelect = document.getElementById('branch');
        data.forEach(branch => {
          let option = document.createElement('option');
          option.value = branch.id;
          option.text = branch.name;
          branchSelect.add(option);
        });
      });
  
    // When a branch is selected, populate the facilities dropdown
    document.getElementById('branch').addEventListener('change', function() {
      var branchId = this.value;
      fetch(`get-facilities/${branchId}/`)
        .then(response => response.json())
        .then(data => {
          let facilitySelect = document.getElementById('facility');
          facilitySelect.innerHTML = '<option value="">Select a facility</option>'; // Clear previous options
          data.forEach(facility => {
            let option = document.createElement('option');
            option.value = facility.id;
            option.text = facility.name;
            facilitySelect.add(option);
          });
        });
    });
  
    // When a facility is selected, fetch the product, current stock quantity, and capacity
document.getElementById('facility').addEventListener('change', function() {
var facilityId = this.value;
fetch(`get-product/${facilityId}/`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('product').value = data.product_name || "None";
        document.getElementById('quantity').value = data.quantity || 0;
        document.getElementById('capacity').value = data.capacity;

        // Store currentQuantity and capacity in JavaScript for client-side validation
        var currentQuantity = data.quantity;
        var capacity = data.capacity;

        // Use these values for client-side validation when the form is submitted
        document.getElementById('inventoryForm').addEventListener('submit', function(event) {
            event.preventDefault();  // Prevent the form from submitting immediately

            var newSupply = parseFloat(document.getElementById('new_quantity').value);

            // Check if the new supply + current quantity exceeds the capacity
            if (currentQuantity + newSupply > capacity) {
                alert('Error: The new supply exceeds the facility capacity.');
                return;
            }

            // Proceed with form submission
            fetch('update/', {
                method: 'POST',  // Ensure that it's a POST request
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
                },
                body: JSON.stringify({
                    branch: document.getElementById('branch').value,
                    facility: document.getElementById('facility').value,
                    product: document.getElementById('product').value,
                    current_quantity: currentQuantity,
                    new_quantity: newSupply
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    alert('Inventory updated successfully!');
                    // Optionally, update the current quantity in the UI
                    document.getElementById('quantity').value = data.new_quantity;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
});

function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
const cookies = document.cookie.split(';');
for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    // Does this cookie string begin with the name we want?
    if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
        }
    }
}
return cookieValue;
}
  

