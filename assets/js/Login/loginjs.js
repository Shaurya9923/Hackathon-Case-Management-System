function validate(){
 
    var password=document.getElementById("loginPassword").value;
    if(password.length <8){
        document.getElementById('validationMessageForPassword').innerHTML="Please enter password of atleast 8 characters";
        return false;
    }
    if(password.length >16){
        document.getElementById('validationMessageForPassword').innerHTML="Please enter password of less than 16 characters";
        return false;
    }
}        