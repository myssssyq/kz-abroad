const form = document.querySelector('#register_form');
const button = document.querySelector('#button');

const pass_reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
const letters = /^[a-zA-Z]{1,30}/;
const email_re = /^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$/;

var password_pass = 0;
var password_check_pass = 0;
var login_pass = 0;
var first_name_pass = 0;
var last_name_pass = 0;
var email_pass = 0;

let first_name = form.elements.namedItem('first_name');
let first_name_label = document.querySelector('#first_name_label');
let last_name = form.elements.namedItem('last_name');
let last_name_label = document.querySelector('#last_name_label');
let login = form.elements.namedItem('login');
let login_label = document.querySelector('#login_label');
let email = form.elements.namedItem('email');
let email_label = document.querySelector('#email_label');
let password = form.elements.namedItem('password');
let password_label = document.querySelector('#password_label');
let password_check = form.elements.namedItem('password_check');
let password_check_label = document.querySelector('#password_check_label');

first_name.addEventListener('input', validate);
last_name.addEventListener('input', validate);
login.addEventListener('input', validate);
email.addEventListener('input', validate);
password.addEventListener('input', validate);
password_check.addEventListener('input', validate);

form.addEventListener('submit', function (e){
if (password_pass +
password_check_pass +
login_pass +
first_name_pass +
last_name_pass +
email_pass != 6) {
  e.preventDefault();
} else {}
//alert(password_pass + password_check_pass);


})




function validate (e) {

  if (e.target.name == "password") {

  if (pass_reg.test(e.target.value)) {
    password_label.className = 'hidden';
    password_pass = 1;
  } else {
    password_label.className = '';
    password_pass = 0;
  }

  }
  if (e.target.name == "password_check") {
  if (e.target.value == password.value){
    password_check_pass = 1;
    password_check_label.className = 'hidden';
  } else {
    password_check_pass = 0;
    password_check_label.className = '';
  }
  }
  if (e.target.name == "first_name") {
    if (letters.test(e.target.value) && e.target.value.length < 30) {
      first_name_pass = 1;
      first_name_label.className = 'hidden';
    } else {
      first_name_label.className = '';
      first_name_pass = 0;
    }
  }
  if (e.target.name == "last_name") {
    if (letters.test(e.target.value) && e.target.value.length < 30) {
      last_name_pass = 1;
      last_name_label.className = 'hidden';
    } else {
      last_name_pass = 0;
      last_name_label.className = '';
    }
  }
  if (e.target.name == "login") {
    if (letters.test(e.target.value) && e.target.value.length < 30) {
      login_pass = 1;
      login_label.className = 'hidden';
    } else {
      login_pass = 0;
      login_label.className = '';
    }
  }
  if (e.target.name == "email") {
    if (email_re.test(e.target.value) && e.target.value.length < 255) {
      email_pass = 1;
      email_label.className = 'hidden';
    } else {
      email_pass = 0;
      email_label.className = '';
    }
  }
  if (password_pass +
  password_check_pass +
  login_pass +
  first_name_pass +
  last_name_pass +
  email_pass != 6) {
    var button = document.querySelector('#button');
    button.disabled = true
    var form_label = document.querySelector('#label_form');
    form_label.innerHTML = password_pass +
    password_check_pass +
    login_pass +
    first_name_pass +
    last_name_pass +
    email_pass;
  } else {
      var button = document.querySelector('#button');
      button.disabled = false
  }
}
