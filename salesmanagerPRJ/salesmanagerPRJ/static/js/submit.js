$(document).on('submit', '#submit-form', function(e){
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: '/submit',
        data:{
            dictionariesOfDataValues,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
            alert(data)
        }
    });
});

// realtime update
setInterval(function(){
    $.ajax({
        type:'GET',
        url: "/getSales/{{agent}}/",
        success: function(response){
            console.log(response) // for testing
            $("#display").empty();
            for (var key in response.sales)
            {
                var temp = "<div class= 'container darker'><b>" +response.sales[key].user+"</b><p>"+response.messages[key].value+"</p><span class = 'time-left'>"+response.messages[ket].date+"</span></div"
                $("display").append(temp);
            }
        },
        error: function(response){
            alert("An error occured")
        }
    });
}, 1000);
$.ajax