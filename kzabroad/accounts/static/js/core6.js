let notification_delete = document.querySelector('#delete_notifications');
notification_delete.addEventListener('click', delete_notifications);

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
    error       : errorFunction
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
