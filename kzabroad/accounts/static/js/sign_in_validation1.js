const form = document.querySelector('#register_form');
const button = document.querySelector('#button_finish_form');

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
let city_input = form.elements.namedItem("city_choice");
//city_check_button.setAttribute('data-step', "step-dot-3");
//city_check_button.addEventListener('click', city_validate)

let city_check_button = document.querySelector('#city_check_button');
let first_part_button = document.querySelector('#first_part_button');
let second_part_button = document.querySelector('#second_part_button');

first_part_button.setAttribute('data-step', "step-dot-2");
second_part_button.setAttribute('data-step', "step-dot-4");

/*function city_validate (e) {
  alert(1)
  e.preventDefault();
  e.setAttribute('data-step', "step-dot-3");
  alert(2)
}*/

first_name.addEventListener('input', validate_first_part);
last_name.addEventListener('input', validate_first_part);
login.addEventListener('input', validate_first_part);
email.addEventListener('input', validate_first_part);
password.addEventListener('input', validate_second_part);
password_check.addEventListener('input', validate_second_part);
city_input.addEventListener('input', city_validate);

function city_validate (e)
{
  if (city_input.value != ""){
  $.ajax({
    type        : 'GET',
    data        : {"city_value": city_input.value}, // our form data
    dataType    : 'json', // what type of data do we expect back from the server
    //success     : successFunction,
    success: function (data) {
          city_check_button.setAttribute('data-step', "step-dot-4");
        },
    error: function (data) {
          city_check_button.setAttribute('data-step', "step-dot-3");
        }
    //error       : errorFunction
  });
  }
  else{
    city_check_button.setAttribute('data-step', "step-dot-4");
  }
}
/*function successFunction(msg) {
  alert(msg.message)
  if (msg.message == 'success') {
      alert(2)
      city_check_button.setAttribute('data-step', "step-dot-4");
  }
}
function errorFunction(msg) {
  alert(1)
  city_check_button.setAttribute('data-step', "step-dot-3");
}*/


/*
var search = document.querySelector('#search');
var results = document.querySelector('#searchresults');
var templateContent = document.querySelector('#resultstemplate').content;
search.addEventListener('keyup', function handler(event) {
    while (results.children.length) results.removeChild(results.firstChild);
    var inputVal = new RegExp(search.value.trim(), 'i');
    var set = Array.prototype.reduce.call(templateContent.cloneNode(true).children, function searchFilter(frag, item, i) {
        if (inputVal.test(item.textContent) && frag.children.length < 6) frag.appendChild(item);
        return frag;
    }, document.createDocumentFragment());
    results.appendChild(set);
});*/
//alert(78)
function validate_first_part (e)
{
  if (e.target.name == "first_name")
  {
    if (letters.test(e.target.value) && e.target.value.length < 30)
    {
      first_name_pass = 1;
      first_name_label.className = 'hidden';
    } else
    {
      first_name_label.className = '';
      first_name_pass = 0;
    }
  }
  if (e.target.name == "last_name")
  {
    if (letters.test(e.target.value) && e.target.value.length < 30)
    {
      last_name_pass = 1;
      last_name_label.className = 'hidden';
    } else
    {
      last_name_pass = 0;
      last_name_label.className = '';
    }
  }
  if (e.target.name == "login")
  {
    if (letters.test(e.target.value) && e.target.value.length < 30)
    {
      login_pass = 1;
      login_label.className = 'hidden';
    } else {
      login_pass = 0;
      login_label.className = '';
    }
  }
  if (e.target.name == "email")
  {
    if (email_re.test(e.target.value) && e.target.value.length < 255)
    {
      email_pass = 1;
      email_label.className = 'hidden';
    } else
    {
      email_pass = 0;
      email_label.className = '';
    }
  }
  if (email_pass + login_pass + first_name_pass + last_name_pass == 4)  {
    first_part_button.setAttribute('data-step', "step-dot-3");
  }
  else
  {
    first_part_button.setAttribute('data-step', "step-dot-2");
  }
}

function validate_second_part (e) {

  if (e.target.name == "password")
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
    if (e.target.value == password_check.value)
    {
      password_check_pass = 1;
      password_check_label.className = 'hidden';
    }
    else
    {
      password_check_pass = 0;
      password_check_label.className = '';
    }

  }
  if (e.target.name == "password_check")
  {
    if (e.target.value == password.value)
      {
        password_check_pass = 1;
        password_check_label.className = 'hidden';
      }
      else
      {
        password_check_pass = 0;
        password_check_label.className = '';
      }
  }
  if (password_pass + password_check_pass == 2)
  {
    second_part_button.setAttribute('data-step', "step-dot-5");
  }
  else
  {
    second_part_button.setAttribute('data-step', "step-dot-4");
  }
}
