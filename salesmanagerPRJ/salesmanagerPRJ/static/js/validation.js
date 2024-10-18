
const form =  document.querySelector('#staff');
const titleInput =document.querySelector('#titleField');
const firstnameField = document.querySelector('#fnameField');
const surnameField = document.querySelector('#snameField');
const phoneField = document.querySelector('#phoneField');
const emailField = document.querySelector('#emailField');
const designationField = document.querySelector('#designationField');
const branchIDField = document.querySelector('#branchIDField');
const dobField = document.querySelector('#dobField');
const emplymentdateField = document.querySelector('#emplymentdateField');

form.addEventListener('submit', (event)=>{

    validateInputs();
    if(isValid()==true){
        form.submit();
    } else {
        event.preventDefault();

    }
});

function isValid(){
    const inputContainers = form.querySelectorAll('.form-group');
    let result = true;
    inputContainers.forEach((container)=>{
        if (container.classList.contains('error')){
            result = false;
        }
    });
    return result;
}


function validateInputs(){
    //title
    if (titleInput.value.trim()==''){
        setError(titleInput, 'Title can not be empty');
    } else {
        setSuccess(titleInput);
    }

    //fnameField
    if (firstnameField.value.trim()==''){
        setError(firstnameField, 'First Name Can not empty');
    } else if ((firstnameField.value.trim().length >100) || (firstnameField.value.trim().length <3)) {
        setError(firstnameField, 'First name is too long, Name can not be more than 100 characters');
    } else {
        setSuccess(firstnameField);
    }

    //snameField
    if (surnameField.value.trim()==''){
        setError(surnameField, 'Surname Can not empty');
    } else if ((surnameField.value.trim().length >100) || (surnameField.value.trim().length <3)){
        setError(surnameField, 'Surname is too long, Name can not be more than 100 characters');
    } else {
        setSuccess(surnameField);
    }
    //phoneField
    if (phoneField.value.trim()==''){
        setError(phoneField, 'Invalid phone number');
    } else if (isPhoneValid(phoneField.value)) {
        setSuccess(phoneField);
    } else {
        setError(phoneField,"Invalid phone number");
    }

    //emailField
    if (emailField.value.trim()==''){
        setError(emailField, 'Invalid email address');
    } else if (isEmailValid(emailField.value)) {
        setSuccess(emailField);
    } else {
        setError(emailField,"Invalid email address");
    }

    //designationField
    if (designationField.value.trim()==''){
        setError(designationField, 'Designation Can not empty');
    } else {
        setSuccess(surnameField);
    }

    //branchIDField
    if (branchIDField.value.trim()==''){
        setError(branchIDField, 'Branch Name Can not empty');
    } else {
        setSuccess(branchIDField);
    }

    //dobField
    //const validDob = validateDate(dobField);
    console.log('DOB:',validDob);
    if (validateDate(dobField) == false) {
        setError(dobField, "Invalid date");
    } else {
        setSuccess(dobField);
    }

    //emplymentdateField
    //const validEmployementDate =validateDate(emplymentdateField);
    console.log('Employment',validEmployementDate);
    if (validateDate(emplymentdateField) == false) {
        setError(emplymentdateField,"Invalid date");
    } else {
        setSuccess(emplymentdateField);
    }

}

function validateDate(date){
    const valid = false;
    const currentDate = new Date(); //current date
    if (!isNaN(Date(date))) {
        valid = true;
    } else if  (date < currentDate){
        valid = false;
    } else {
        valid = true;
    }
    return valid;
}

function setError(element, message){
    const parent = element.parentElement;
    if (parent.classList.contains('success')){
        parent.classList.remove('success');
    }
    parent.classList.add('error');
    const para = parent.querySelector('p');
    para.textContent = message;
}


function setSuccess(element){
    const parent = element.parentElement;
    if (parent.classList.contains('error')){
        parent.classList.remove('error');
    }
    parent.classList.add('success');
}

function isEmailValid(email){
    const reg = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\"))@(([^<>()[\]\.;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
}

function isPhoneValid(phone){
    const regtern = /^\0+d{10}$/;
}
