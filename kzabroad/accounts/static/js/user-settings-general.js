const general_form = document.querySelector('#general_form');
let general_submit_button = document.querySelector('#general_submit_button');
let general_form_message = document.querySelector('#general_form_message')

const letters = /^[a-zA-Z]+$/;

let first_name = general_form.elements.namedItem('first_name');
let first_name_label = document.querySelector('#first_name_label');
let last_name = general_form.elements.namedItem('last_name');
let last_name_label = document.querySelector('#last_name_label');

let city = general_form.elements.namedItem('city_input')
let city_label = document.querySelector('#city_label')

first_name.addEventListener('input', validate);
last_name.addEventListener('input', validate);

city.addEventListener('input', cityInputValidate);

general_form.addEventListener('submit', generalFormValidate)

function generalFormValidate(e)
{
  e.preventDefault()
  $.ajax({
    type        : 'POST',
    data        : $('#general_form').serialize(),
    dataType    : 'json',
    success: function (data)
    {
      //first_name.value = data.first_name
    }
  });
  general_form_message.className = "";
}

function cityInputValidate(e)
{
  $.ajax({
    type        : 'GET',
    url         : '/api/validate_city',
    data        : {"city_value": city_input.value},
    dataType    : 'json',
    success: function (data) {
          city_label.className = "hidden"
          city_pass = 1
        },
    error: function (data) {
          city_label.className = ""
          city_pass = 0
        }
  });
  if (first_name_pass + last_name_pass + city_pass == 3)
  {
    general_submit_button.disabled = false;
  }
  else
  {
    general_submit_button.disabled = true;
  }
}

var first_name_pass = 1;
var last_name_pass = 1;
var city_pass = 1;

function validate(e)
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
  if (first_name_pass + last_name_pass + city_pass == 3)
  {
    general_submit_button.disabled = false;
  }
  else
  {
    general_submit_button.disabled = true;
  }
}
