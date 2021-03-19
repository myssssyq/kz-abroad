const form = document.querySelector('#data_edit_form');

let tiktok = form.elements.namedItem('tiktok');
let tiktok_label = document.querySelector('#tiktok_label');
let vk = form.elements.namedItem('vk');
let vk_label = document.querySelector('#vk_label');
let instagram = form.elements.namedItem('instagram');
let instagram_label = document.querySelector('#instagram_label');
let facebook = form.elements.namedItem('facebook');
let facebook_label = document.querySelector('#facebook_label');
let twitter = form.elements.namedItem('twitter');
let twitter_label = document.querySelector('#twitter_label');

let occupation = form.elements.namedItem('occupation_choice');
let occupation_label = document.querySelector('#occupation_label');

const tiktok_reg = /^(https?:\/\/)?((w{3}\.)?)vm.tiktok.com\/.*/i;
const vk_reg = /^(https?:\/\/)?((w{3}\.)?)vk.com\/.*/i;
const instagram_reg = /^(https?:\/\/)?((w{3}\.)?)instagram.com\/.*/i;
const facebook_reg = /^(https?:\/\/)?((w{3}\.)?)facebook.com\/.*/i;
const twitter_reg = /^(https?:\/\/)?((w{3}\.)?)twitter.com\/.*/i;

var tiktok_pass = 1;
var vk_pass = 1;
var instagram_pass = 1;
var facebook_pass = 1;
var twitter_pass = 1;

tiktok.addEventListener('input', validate);
vk.addEventListener('input', validate);
instagram.addEventListener('input', validate);
facebook.addEventListener('input', validate);
twitter.addEventListener('input', validate);

occupation.addEventListener('input', occupationValidate);

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
});

function occupationValidate (e)
{
  $.ajax({
    type        : 'GET',
    data        : {"occupation_value": occupation.value},  //our form data
    dataType    : 'json', // what type of data do we expect back from the server
    success     : successFunction,
    error       : errorFunction
  });
}
function successFunction(msg)
{
  if (msg.message != '')
  {
    occupation_label.innerHTML = "Did you mean " + msg.message + "?"
    occupation_label.className = ""
  }
}
function errorFunction(msg)
{
  occupation_label.className = "hidden"
}

function validate (e) {

var button = document.querySelector('#edit_button');
var form_label = document.querySelector('#edit_label');
//-------------------------------------
if (e.target.name == "tiktok")
{
  if (tiktok_reg.test(e.target.value) || e.target.value.length == 0)
  {
    tiktok_pass = 1
    tiktok_label.className = 'hidden'
  }
  else
  {
    tiktok_pass = 0
    tiktok_label.className = ''
  }
}
//-------------------------------------
if (e.target.name == "vk")
{
  if (vk_reg.test(e.target.value) || e.target.value.length == 0)
  {
    vk_pass = 1
    vk_label.className = 'hidden'
  }
  else
  {
    vk_pass = 0
    vk_label.className = ''
  }
}
//-------------------------------------
if (e.target.name == "instagram")
{
  if (instagram_reg.test(e.target.value) || e.target.value.length == 0)
  {
    instagram_pass = 1
    instagram_label.className = 'hidden'
  }
  else
  {
    instagram_pass = 0
    instagram_label.className = ''
  }
}
//-------------------------------------
if (e.target.name == "facebook")
{
  if (facebook_reg.test(e.target.value) || e.target.value.length == 0)
  {
    facebook_pass = 1
    facebook_label.className = 'hidden'
  }
  else
  {
    facebook_pass = 0
    facebook_label.className = ''
  }
}
//-------------------------------------
if (e.target.name == "twitter")
{
  if (twitter_reg.test(e.target.value) || e.target.value.length == 0)
  {
    twitter_pass = 1
    twitter_label.className = 'hidden'
  }
  else
  {
    twitter_pass = 0
    twitter_label.className = ''
  }
}
//-------------------------------------
if
(
tiktok_pass +
vk_pass +
instagram_pass +
facebook_pass +
twitter_pass == 5
)
{
  button.disabled = false
}
else
{
  button.disabled = true
}
//-------------------------------------
}
