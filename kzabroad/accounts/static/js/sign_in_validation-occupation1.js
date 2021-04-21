const numbers = /^[0-9]+$/;

let highschoolName = form.elements.namedItem('highschool-name');
let universityName = form.elements.namedItem('university-name');
let workName = form.elements.namedItem('work-name');

let highschoolPosition = form.elements.namedItem('highschool-position');
let universityPosition = form.elements.namedItem('university-position');
let workPosition = form.elements.namedItem('work-position');

let highschoolDescription = form.elements.namedItem('highschool-description');
let universityDescription = form.elements.namedItem('university-description');
let workDescription = form.elements.namedItem('work-description');

let highschoolYearFrom = form.elements.namedItem('highschool-year_from');
let universityYearFrom = form.elements.namedItem('university-year_from');
let workYearFrom = form.elements.namedItem('work-year_from');

let highschoolYearTo = form.elements.namedItem('highschool-year_to');
let universityYearTo = form.elements.namedItem('university-year_to');
let workYearTo = form.elements.namedItem('work-year_to');

let highschoolLabel = document.querySelector('#highschool-form_label');
let universityLabel = document.querySelector('#university-form_label');
let workLabel = document.querySelector('#work-form_label');

let highschoolDateLabel = document.querySelector('#highschool-year_span_label');
let universityDateLabel = document.querySelector('#university-year_span_label');
let workDateLabel = document.querySelector('#work-year_span_label');

const nextStepButton = document.querySelector('#next_step_button');

highschoolName.addEventListener('input', occupationValidate);
universityName.addEventListener('input', occupationValidate);
workName.addEventListener('input', occupationValidate);

highschoolPosition.addEventListener('input', occupationValidate);
universityPosition.addEventListener('input', occupationValidate);
workPosition.addEventListener('input', occupationValidate);

highschoolDescription.addEventListener('input', occupationValidate);
universityDescription.addEventListener('input', occupationValidate);
workDescription.addEventListener('input', occupationValidate);

highschoolYearFrom.addEventListener('input', occupationValidate);
universityYearFrom.addEventListener('input', occupationValidate);
workYearFrom.addEventListener('input', occupationValidate);

highschoolYearTo.addEventListener('input', occupationValidate);
universityYearTo.addEventListener('input', occupationValidate);
workYearTo.addEventListener('input', occupationValidate);

var highschool_year_from_pass = 0;
var highschool_year_to_pass = 0;
var university_year_from_pass = 0;
var university_year_to_pass = 0;
var work_year_from_pass = 0;
var work_year_to_pass = 0;

var highschool_pass = 1;
var university_pass = 1;
var work_pass = 1;

function occupationValidate(e)
{
  if (e.target.name == "highschool-name"
  || e.target.name == "highschool-position"
  || e.target.name == "highschool-description"
  || e.target.name == "highschool-year_from"
  || e.target.name == "highschool-year_to")
  {
    if (e.target.name == "highschool-year_from")
    {
      if (numbers.test(e.target.value) && e.target.value.length == 4)
      {
        highschoolDateLabel.className = "hidden"
        highschool_year_from_pass = 1
      }
      else
      {
        highschoolDateLabel.className = ""
        highschool_year_from_pass = 0
      }
    }
    if (e.target.name == "highschool-year_to")
    {
      if (numbers.test(e.target.value) && e.target.value.length == 4)
      {
        highschoolDateLabel.className = "hidden"
        highschool_year_to_pass = 1
      }
      else
      {
        highschoolDateLabel.className = ""
        highschool_year_to_pass = 0
      }
    }
    if (highschoolName.value == ""
    || highschoolPosition.value == ""
    || highschoolDescription.value == ""
    || highschoolYearFrom.value == ""
    || highschoolYearTo.value == "")
    {
      highschoolLabel.className = ""
      highschool_pass = 0
    }
    else
    {
      highschoolLabel.className = "hidden"
      if (highschool_year_from_pass + highschool_year_to_pass == 2)
      {
        highschool_pass = 1;
      }
      else
      {
        highschool_pass = 0
      }
    }
    if (highschoolName.value == ""
    && highschoolPosition.value == ""
    && highschoolDescription.value == ""
    && highschoolYearFrom.value == ""
    && highschoolYearTo.value == "")
    {
      highschool_pass = 1;
      highschoolLabel.className = "hidden";
      highschoolDateLabel.className = "hidden";
    }
  }
  if (e.target.name == "university-name"
  || e.target.name == "university-position"
  || e.target.name == "university-description"
  || e.target.name == "university-year_from"
  || e.target.name == "university-year_to")
  {
    if (e.target.name == "university-year_from")
    {
      if (numbers.test(e.target.value) && e.target.value.length == 4)
      {
        universityDateLabel.className = "hidden"
        university_year_from_pass = 1
      }
      else
      {
        universityDateLabel.className = ""
        university_year_from_pass = 0
      }
    }
    if (e.target.name == "university-year_to")
    {
      if (numbers.test(e.target.value) && e.target.value.length == 4)
      {
        universityDateLabel.className = "hidden"
        university_year_to_pass = 1
      }
      else
      {
        universityDateLabel.className = ""
        university_year_to_pass = 0
      }
    }
    if (universityName.value == ""
    || universityPosition.value == ""
    || universityDescription.value == ""
    || universityYearFrom.value == ""
    || universityYearTo.value == "")
    {
      universityLabel.className = ""
      university_pass = 0
    }
    else
    {
      universityLabel.className = "hidden"
      if (university_year_from_pass + university_year_to_pass == 2)
      {
        university_pass = 1;
      }
      else
      {
        university_pass = 0
      }
    }
    if (universityName.value == ""
    && universityPosition.value == ""
    && universityDescription.value == ""
    && universityYearFrom.value == ""
    && universityYearTo.value == "")
    {
      university_pass = 1;
      universityLabel.className = "hidden";
      universityDateLabel.className = "hidden";
    }
  }
  if (e.target.name == "work-name"
  || e.target.name == "work-position"
  || e.target.name == "work-description"
  || e.target.name == "work-year_from"
  || e.target.name == "work-year_to")
  {
    if (e.target.name == "work-year_from")
    {
      if (numbers.test(e.target.value) && e.target.value.length == 4)
      {
        workDateLabel.className = "hidden"
        work_year_from_pass = 1
      }
      else
      {
        workDateLabel.className = ""
        work_year_from_pass = 0
      }
    }
    if (e.target.name == "work-year_to")
    {
      if (numbers.test(e.target.value) && e.target.value.length == 4)
      {
        workDateLabel.className = "hidden"
        work_year_to_pass = 1
      }
      else
      {
        workDateLabel.className = ""
        work_year_to_pass = 0
      }
    }
    if (workName.value == ""
    || workPosition.value == ""
    || workDescription.value == ""
    || workYearFrom.value == ""
    || workYearTo.value == "")
    {
      workLabel.className = ""
      work_pass = 0
    }
    else
    {
      workLabel.className = "hidden"
      if (work_year_from_pass + work_year_to_pass == 2)
      {
        work_pass = 1;
      }
      else
      {
        work_pass = 0
      }
    }
    if (workName.value == ""
    && workPosition.value == ""
    && workDescription.value == ""
    && workYearFrom.value == ""
    && workYearTo.value == "")
    {
      work_pass = 1;
      workLabel.className = "hidden";
      workDateLabel.className = "hidden";
    }
  }
  if (highschool_pass + university_pass + work_pass == 3)
  {
    nextStepButton.setAttribute('data-step', "step-dot-2");
  }
  else
  {
    nextStepButton.setAttribute('data-step', "step-dot-1");
  }
}
