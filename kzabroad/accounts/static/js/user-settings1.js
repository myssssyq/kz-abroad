const pass_reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
const form = document.querySelector('#security_form');
const form_label = document.querySelector('#form_message');

let submit_button = document.querySelector('#security_form_submit');

let password = document.querySelector('#password_input');
let password_repeat = document.querySelector('#repeat_password_input');
let password_label = document.querySelector('#password_label');
let repeat_password_label = document.querySelector('#repeat_password_label');

password.addEventListener('input', validate);
password_repeat.addEventListener('input', validate);

form.addEventListener('submit', formValidate);

var password_pass = 0;
var password_repeat_pass = 0;

function formValidate (e)
{
  e.preventDefault();
  form_label.innerHTML= "Password can not be changed"
  if (password_pass + password_repeat_pass == 2)
  {
  $.ajax({
    type        : 'GET',
    data        : {"password": password.value},  //our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : successPasswordFunction,
    error       : errorPasswordFunction
  });
  }
}

function successPasswordFunction(msg)
{
  password_pass = 0;
  password_repeat_pass = 0;
  form_label.innerHTML= "Password was changed succesfuly"
  password.value = ""
  password_repeat.value = ""
}

function errorPasswordFunction(msg)
{
  form_label.innerHTML= "Password can not be changed"
}

function validate (e)
{
  if (e.target.name == "password_input")
  {
    if (pass_reg.test(e.target.value))
    {
      password_label.className = 'hidden';
      password_pass = 1;
    }
    else
    {
      password_label.className = '';
      password_pass = 0;
    }
    if (e.target.value == password_repeat.value)
    {
      password_repeat_pass = 1;
      repeat_password_label.className = 'hidden';
    }
    else
    {
      password_repeat_pass = 0;
      repeat_password_label.className = '';
    }
  }
  if (e.target.name == "repeat_password_input")
  {
    if (e.target.value == password.value)
      {
        password_repeat_pass = 1;
        repeat_password_label.className = 'hidden';
      }
      else
      {
        password_repeat_pass = 0;
        repeat_password_label.className = '';
      }
  }
}
