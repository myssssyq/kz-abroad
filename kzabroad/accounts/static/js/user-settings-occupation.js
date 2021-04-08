const add_occupation_form = document.querySelector('#add_occupation_form');
let add_occupation_submit_button = document.querySelector('#add_occupation_submit_button');

add_occupation_submit_button.disabled = true

let name = add_occupation_form.elements.namedItem('name');
let position = add_occupation_form.elements.namedItem('position');
let description = add_occupation_form.elements.namedItem('description');
let year_from = add_occupation_form.elements.namedItem('year_from');
let year_to = add_occupation_form.elements.namedItem('year_to');
let year_span_label = document.querySelector('#year_span_label')

const numbers = /^[0-9]+$/;

year_from.addEventListener('input', validate);
year_to.addEventListener('input', validate);
name.addEventListener('input', validate);
description.addEventListener('input', validate);
position.addEventListener('input', validate);


var year_from_pass = 0;
var year_to_pass = 0;
var name_pass = 0;
var description_pass = 0;
var position_pass = 0;




function validate(e)
{
  if (e.target.name == "year_from")
  {
    if (numbers.test(e.target.value) && e.target.value.length == 4)
    {
      year_from_pass = 1;
      year_span_label.className = "hidden"
    }
    else
    {
      year_from_pass = 0;
      year_span_label.className = ""
    }
  }
  if (e.target.name == "year_to")
  {

    if (numbers.test(e.target.value) && e.target.value.length == 4)
    {
      year_to_pass = 1;
      year_span_label.className = "hidden"
    }
    else
    {
      year_to_pass = 0;
      year_span_label.className = ""
    }
  }
  if (e.target.name == "name")
  {
    if (e.target.value.length != 0)
    {
      name_pass = 1;
    }
    else
    {
      name_pass = 0
    }
  }
  if (e.target.name == "description")
  {
    if (e.target.value.length != 0)
    {
      description_pass = 1
    }
    else
    {
      description_pass = 0
    }
  }
  if (e.target.name == "position")
  {
    if (e.target.value.length != 0)
    {
      position_pass = 1
    }
    else
    {
      position_pass = 0
    }
  }
  if (year_from_pass + year_to_pass + name_pass + description_pass + position_pass == 5)
  {
    add_occupation_submit_button.disabled = false
  }
  else
  {
    add_occupation_submit_button.disabled = true
  }
}
