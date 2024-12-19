document.addEventListener('DOMContentLoaded', function (event) {
    event.preventDefault();

    document.getElementById('bulkshift').addEventListener('change', function() {
        var bulkShiftCkeck = this.value;
        console.log(bulkShiftCkeck);

        if (bulkShiftCkeck.checked)  {

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
            mapping = JSON.stringify(mapping);

            // ajax call
            var url = "bukl-shifts/"
            fetch(url, {
                method:'POST',
                headers:{
                 'Content-Type':'application/json',
                 'X-CSRFToken':  csrftoken,
                }, 
                body:JSON.stringify({'post_data':mapping}) //JavaScript object of data to POST
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
    
    /*if (data.error){
        alert(`Error: ${data.error}`);
    } else {
    
        alert('Mapping created successfully');
    }
    middleware toke: '[name=csrfmiddlewaretoken]'
    method: 'GET',
                headers: {
                    'Content-Type':'application/json; charset=utf-8',
                    'X-CSRFToken': document.querySelector('[name=csrf_token]').value
                },
                body: JSON.stringify(mapping) ,
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Data: ', data);
        
              });//.catch(error => console.error('Error:', error));
        }
    
    });
    
    */

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
   var csrftoken = getToken('csrftoken');
   console(csrftoken);