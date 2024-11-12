document.getElementById("staffIDField").addEventListener("change", function() {
    var staffId = this.value;

    // Use Django's URL template tag to dynamically generate the URL
    //const url = "{% url `get_staff` 0 %}".replace("0", staffId);
    console.log(staffId);
    fetch(`get-staff/${staffId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("usernameField").value = data.phonenumber;
            document.getElementById("roleField").value = data.role;
            console.log('data',data);
        });
});