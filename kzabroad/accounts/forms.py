from django import forms
from password_strength import PasswordPolicy
import re
import string
from .models import *

class SignForm(forms.Form):
    first_name = forms.CharField(label="Your name", max_length=30, required=True)
    last_name = forms.CharField(label="Your lastname",max_length=30, required=True)
    email = forms.EmailField(label="Your email", max_length=50, required=True)
    username = forms.CharField(label="Your username",max_length=40, required=True)
    password = forms.CharField(label="Your password",max_length=40,widget=forms.PasswordInput, required=True)
    password_repeat = forms.CharField(label="Your password",max_length=40,widget=forms.PasswordInput, required=True)

    def clean(self):
       cleaned_data = super(SignForm, self).clean()
       username = cleaned_data.get("username")
       first_name = cleaned_data.get("first_name")
       last_name = cleaned_data.get("last_name")
       email = cleaned_data.get("email")
       password = cleaned_data.get("password")
       password_repeat = cleaned_data.get("password_repeat")


       regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
       is_correct = True
       error_context = dict()
       username_wrong = False
       policy_password_first = PasswordPolicy.from_names\
       (
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
            )
       policy_password_second = PasswordPolicy.from_names\
        (
            strength=0.2
        )


       try:
           letter_exist = False
           for letter in username:
               if letter in string.ascii_letters:
                   letter_exist = True
           for letter in username:
               if letter not in string.ascii_letters and letter not in string.digits:
                   username_wrong = True
           if not re.search(regex,email):
               is_correct = False
               error_context['email'] = ''
           if username_wrong or not letter_exist:
               is_correct = False
               error_context['username'] = ''
           if not last_name[0].isupper():
               is_correct = False
               error_context['last_name'] = ''
           if not first_name[0].isupper():
               is_correct = False
               error_context['first_name'] = ''
           if password != password_repeat:
               is_correct = False
               error_context['password'] = 'Passwords dont match'
           if policy_password_first.test(password):
               is_correct = False
               error_context['password'] = ''
           else:
               if policy_password_second.test(password):
                   is_correct = False
                   error_context['password'] = ''

       except:
            pass

       if not is_correct:
           raise forms.ValidationError(error_context)
       return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label="Your username",max_length=40)
    password = forms.CharField(label="Your password",max_length=40, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        is_correct = True
        error_context = dict()

        try:
            checking_user = Account.objects.get(login = username)
            if password == checking_user.password:
                pass
            else:
                is_correct = False
                error_context['password'] = 'Password is not right'
        except:
            is_correct = False
            error_context['username'] = 'This username does not exist'

        if not is_correct:
            raise forms.ValidationError(error_context)
        return cleaned_data

class SearchForm(forms.Form):
    city = forms.CharField(label="City you want to find", max_length=30, required=True)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        city = cleaned_data.get("city")
        return cleaned_data
