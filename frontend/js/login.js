$(function() {
  var $form = $('#login-form');
  $form.submit(function(event) {

    event.preventDefault();

    user = event.target.inputEmail.value;
    password = event.target.inputPassword.value;

    // The below email and password can be sent to the server to authenticate (or something like that)

    console.log(user);
    console.log(password);

    return true;
  });
});