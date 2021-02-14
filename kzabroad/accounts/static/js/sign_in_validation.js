const form = document.querySelector('#register_form');
const pass_reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;

let first_name = form.elements.namedItem('first_name');
let last_name = form.elements.namedItem('last_name');
let login = form.elements.namedItem('login');
let email = form.elements.namedItem('email');
let password = form.elements.namedItem('password');
let password_check = form.elements.namedItem('password_check');

first_name.addEventListener('input', validate);
last_name.addEventListener('input', validate);
login.addEventListener('input', validate);
email.addEventListener('input', validate);
password.addEventListener('input', validate);
password_check.addEventListener('input', validate);

form.addEventListener('submit', function (e){

e.preventDefault();
alert('SUBMITED');


})



function validate (e) {

  if (e.target.name == "password") {
  if (pass_reg.test(e.target.value)) {
    var x = document.querySelector('#label');
    x.innerHTML = 'strong'
  } else {
    var x = document.querySelector('#label');
    x.innerHTML = 'weak'
  }

 }
  /*if (target = 'password'){

    var strength = 0;

    strength += /[A-Z]+/.test(target) ? 1 : 0;
    strength += /[a-z]+/.test(target) ? 1 : 0;
    strength += /[0-9]+/.test(target) ? 1 : 0;
    strength += /[\W]+/.test(target) ? 1 : 0;

    switch(strength) {
        case 3:
            var x = document.querySelector('#label');
            x.innerHTML = 'medium'
            break;
        case 4:
            var x = document.querySelector('#label');
            x.innerHTML = 'strong'
            break;
        default:
            var x = document.querySelector('#label');
            x.innerHTML = 'weak'
            break;
    }
  } */
}
