const buttons = document.getElementsByName("unfriend_button")

for (var i =0; i < buttons.length; i++)
{
  var x = buttons[i].getAttribute("data");
  buttons[i].addEventListener('click', delete_friend.bind(event, x));
}

function delete_friend(e, x)
{
  x.preventDefault()
  var divToDelete = document.querySelector("#friend_div_" + e);
  divToDelete.remove()
  data = {"delete_friend": "", "id" : e}
  $.ajax({
    type        : 'GET',
    data        : data, // our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : function (data) {

                },
    error       : function (data) {

                },
  });
}
