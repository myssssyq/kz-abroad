const form = document.querySelector('#add_city_form');
let add_input = form.elements.namedItem('add');
let message_label = document.querySelector('#message_label');

form.addEventListener("submit", submitHandler);

function submitHandler(e) {
      e.preventDefault();
      $.ajax({
        type        : 'POST',
        url         : '/city/api/validate_city',
        data        : $('#add_city_form').serialize(), // our form data
        dataType    : 'json', // what type of data do we expect back from the server
        success     : successFunction,
        error       : errorFunction
      });
  }
function successFunction(msg) {
      if (msg.message === 'success') {
          form.submit();
      }
  }
function errorFunction(msg) {
      message_label.className = "";
      message_label.innerHTML = "Error occured. This city already exists";
  }
