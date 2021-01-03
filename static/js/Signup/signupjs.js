function validate(){
    /*First Name Validation Start*/ 
    var firstName=document.getElementById('firstName').value;
    var firstNameRegex=/^[A-Za-z]+$/;
    if(firstName.length <3){
        document.getElementById('validationMessageForFirstName').innerHTML="Please enter name more than 3 characters";
        return false;
    }
    if(firstName.length >15){
        document.getElementById('validationMessageForFirstName').innerHTML="Please enter name less than 15 characters";
        return false;
    }
    if(firstNameRegex.test(firstName)){
        document.getElementById('validationMessageForFirstName').innerHTML="";
    }else{
        document.getElementById('validationMessageForFirstName').innerHTML="Please enter alphabets only";
        return false;
    }
    
    /*First Name Validation Ends*/ 

    /*Middle Name Validation Starts*/
    var middleName=document.getElementById('middleName').value;
    var middleNameRegex=/^[A-Za-z]+$/;
    if(middleName.length <3){
        document.getElementById('validationMessageForMiddleName').innerHTML="Please enter name more than 3 characters";
        return false;
    }
    if(middleName.length >15){
        document.getElementById('validationMessageForMiddleName').innerHTML="Please enter name less than 15 characters";
        return false;
    }
    if(middleNameRegex.test(middleName)){
        document.getElementById('validationMessageForMiddleName').innerHTML="";
    }else{
        document.getElementById('validationMessageForMiddleName').innerHTML="Please enter alphabets only";
        return false;
    }
    /* Middle Name Validation Ends*/
    /*Last Name Validation Start*/ 
    var lastName=document.getElementById('lastName').value;
    var lastNameRegex=/^[A-Za-z]+$/;
    if(lastName.length <2){
        document.getElementById('validationMessageForLastName').innerHTML="Please enter name more than 2 characters";
        return false;
    }
    if(lastName.length >15){
        document.getElementById('validationMessageForLastName').innerHTML="Please enter name less than 15 characters";
        return false;
    }
    if(lastNameRegex.test(lastName)){
        document.getElementById('validationMessageForLastName').innerHTML="";
    }else{
        document.getElementById('validationMessageForLastName').innerHTML="Please enter alphabets only";
        return false;
    }
    /*Last Name Validation Ends*/
    /*Email Id Validation Start*/
    var email=document.getElementById('emailId').value;
    if(email.indexOf('@')==0){
        document.getElementById('validationMessageForEmail').innerHTML="Please enter proper email format";
        return false;
    }

    if((email.charAt(email.length-4)!='.') && (email.charAt(email.length-3)!='.')){
        document.getElementById('validationMessageForEmail').innerHTML="Please enter proper email format for .";
        return false;
    }
    /*Password Validation Start*/
    var password=document.getElementById("password").value;
    var cpassword=document.getElementById('confirmPassword').value;
    if(password.length <8){
        document.getElementById('validationMessageForPassword').innerHTML="Please enter password of atleast 8 characters";
        return false;
    }
    if(password.length >16){
        document.getElementById('validationMessageForPassword').innerHTML="Please enter password of less than 16 characters";
        return false;
    }
    if(password==cpassword){
        document.getElementById('validationMessageForPassword').innerHTML="";
    }else{
        document.getElementById('validationMessageForConfirmPassword').innerHTML="Password doesn't match";
        return false;
    }
    /*Password Validation Ends*/
    /*Contact Number Validation Starts*/
    var contactNo=document.getElementById('contactNumber').value;
    if((contactNo.length <10) && (contactNo>10)){
        document.getElementById('validationMessageForContactNumber').innerHTML="Please enter 10 digit number";
        return false;
    }
    if(isNaN(contactNo)){
        document.getElementById('validationMessageForContactNumber').innerHTML="Please enter digits only";
        return false;
    }
    /*Contact Number Validation Ends*/
}                   