const button = document.querySelector('#add_friend_button')

button.addEventListener('click', addFriendFunction)

function addFriendFunction(e)
{
  e.preventDefault;
  $.ajax({
    type        : 'GET',
    data        : {"action":"add_friend"}, // our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : function (data) {
                  e.target.innerHTML = "Request is sent!"
                },
    error       : function (data) {
                  e.target.innerHTML = "Request is already sent!"
                },
  });
}
