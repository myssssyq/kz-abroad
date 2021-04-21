let notification_delete = document.querySelector('#delete_notifications');

notification_delete.addEventListener('click', delete_notifications);

var buttons_accept = document.querySelectorAll('button[name="accept"]');
var buttons_decline = document.querySelectorAll('button[name="decline"]');

//var request_submits = document.getElementsByClassName("request_submits");

for (var i =0; i < (buttons_decline.length); i++)
{
  var x = buttons_accept[i].getAttribute("data-id");
  buttons_accept[i].addEventListener('click', accept_request.bind(event, x));
  buttons_decline[i].addEventListener('click', decline_request.bind(event, x));
}

function accept_request(e, x)
{
  x.preventDefault()
  data = {"action": "accept", "id" : e}
  $.ajax({
    type        : 'GET',
    data        : data, // our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : successRequestFunction,
    error       : function (data) {

                },
  });
}

function decline_request(e, x)
{
  x.preventDefault();
  data = {"action": "decline", "id" : e}
  $.ajax({
    type        : 'GET',
    data        : data, // our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : successRequestFunction,
    error       : function (data) {

                },
  });
}

function delete_notifications(e)
{
  //x = document.querySelector('.messageCheckbox').checked;
  var checkedValue = [];
  var inputElements = document.getElementsByClassName('messageCheckbox');
  for(var i=0; inputElements[i]; ++i)
  {
      if(inputElements[i].checked){
           checkedValue.push({
             "id": inputElements[i].getAttribute("name")
           });
      }
  }
  checkedValue = JSON.stringify(checkedValue)
  $.ajax({
    type        : 'GET',
    data        : checkedValue, // our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : successFunction,
    error       : function (data) {

                },
  });
}

function successFunction(msg)
{
  for (i in msg)
  {
    var divToDelete = document.querySelector("#notificationId" + msg[i]);
    divToDelete.remove()
  }
}

function successRequestFunction(msg)
{
  var divToDelete = document.querySelector("#divRequest" + msg.id);
  divToDelete.remove()
}
