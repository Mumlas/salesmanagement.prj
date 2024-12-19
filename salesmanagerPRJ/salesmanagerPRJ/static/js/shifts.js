
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('inventoryIDField').addEventListener('change', function() {
    var inventoryId = this.value;
    const agentSelected = document.getElementById('staff');
    const postsSelected = document.getElementById('pump');
    const selectedAgentField = document.getElementById('staffArea');
    const selectedPostsField = document.getElementById('pumpArea');

    //Field to display selections
    const mappingField = document.createElement('textarea');
    mappingField.id = 'mappingField';
    mappingField.rows=5;
    mappingField.readOnly = true;
    mappingField.placeholder = 'Agent-Post mappings';
    document.getElementById('shiftForm').appendChild(mappingField);

    // function to updated selected values
    function updatedSelectedValues(selectElement, targetField, existingValues){
      const selectedOptions = Array.from(selectElement.selectedOptions).map(option => option.text);
      const newValues = selectedOptions.filter(value => !existingValues.includes(value));
      const updatedValues = [...existingValues, ...newValues]; // combining existing values and new values

      targetField.value = updatedValues.join(', ');// join all selected values seperated with comma
      return updatedValues;
    }

    
    let selectedAgents =[];
    let seletedPosts = [];
    
    
    //event listeners for agents and posts
    agentSelected.addEventListener('change', function () {
      updatedSelectedValues(agentSelected, selectedAgentField, selectedAgents);
    });
    
    postsSelected.addEventListener('change', function() {
      updatedSelectedValues(postsSelected, selectedPostsField, seletedPosts);
    });
    
    //function ro create mappings
    function createMapping() {
      const selectedAgents = Array.from(agentSelected.selectedOptions).map(option => option.value);
      const selectedPosts = Array.from(postsSelected.selectedOptions).map(option => option.value);

      if (selectedAgents.length !== selectedPosts.length) {
        mappingField.value = 'Error: Number of agents and posts must match for one-to-one mapping.';
        return;
      }

      const mapping = selectedAgents.map((agent, index) => ({
        agent:agent,
        post: selectedPosts[index],
      }));

      mappingField.value = mapping.map(pair => `Agent: ${pair.agent} -> Post ${pair.post}`).join('\n');
      return mapping;
    }

    //fetch branch base on the inventory
    fetch(`get-branch/${inventoryId}/`)
      .then(response => response.json())
      .then(data => {
        var branchSelect = document.getElementById('branchid');
        branchSelect.innerHTML = ''; // Clear existing options
        var defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select Branch';
        branchSelect.appendChild(defaultOption); // add default placeholder 

        //populate facility options based on the fetched data
        data.forEach(branch => {
          var option = document.createElement('option');
          option.value = branch.id;
          option.textContent = branch.name;
          branchSelect.appendChild(option)
        });
      });
  });

    
  document.getElementById('branchid').addEventListener('change', function() {
    var branchId = document.getElementById('branchid').value;
    var inventoryId = document.getElementById('inventoryIDField').value;
    
    console.log('Branch ', branchId);
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
    fetch(`get-facilities/${inventoryId}/`)
      .then(response => response.json())
      .then(data => {
        var facilitySelect = document.getElementById('facilityid');
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

  // Facility event listener
  document.getElementById('facilityid').addEventListener('change', function() {
    var facilityId=document.getElementById('facilityid').value;
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
    var branchId=document.getElementById('branchid').value;
    var facilityId=document.getElementById('facilityid').value;
    // Make an AJAX request to fetch the facilities based on the selected branch
    fetch(`get-products/${facilityId}/${branchId}/`)
      .then(response => response.json())
      .then(data => {
      // Add default placeholder option
        // Populate facility options based on the fetched data
        document.getElementById('product').value = data.product_name;
        document.getElementById('stock').value = data.inStock;
      });
  });

  var checkbox = document.querySelector("input[name=bulkshift]");
  var bulkShiftCkeck = document.getElementById('bulkshift');
  console.log(bulkShiftCkeck.checked);

  checkbox.addEventListener('change', function(){
      if (bulkShiftCkeck.checked) {
        console.log(bulkShiftCkeck.checked);
  
          const agents = Array.from(document.getElementById('staff').selectedOptions).map(option => option.value);
          const pumps = Array.from(document.getElementById('pump').selectedOptions).map(option => option.value);
      
          // selected staff equal selected pump
          if (agents.length != pumps.length) {
              alert('Please select an equal number of pump attendant (staff) and pump for one-to-one mapping');
              return;
          }
      
          const mapping = agents.map((agent, index) => ({agent:String(agent), pump: String(pumps[index]) }));
      
          console.log('Mapping: ', mapping);
          console.log('Mapping: ', JSON.stringify(mapping));
  
          // ajax call
          //var url = "bulk-shifts/"
          fetch(`bulk-shifts/`, {
              method:'POST',
              headers:{
              'Content-Type':'application/json',
              'X-CSRFToken':  document.querySelector('[name=csrfmiddlewaretoken]').value,
              }, 
              body: JSON.stringify({'mapping': mapping}) //JavaScript object of data to POST
            })
            .then((response) => {
                return response.json(); //converts response to json
            })
            .then((data) => {
                console.log('data:',data)
              //Perform actions with the response data from the view
            });
      }
  });
});

function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0,name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
 }
