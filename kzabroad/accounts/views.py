from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .forms import *
from .models import *
import cities.views as cityviews
from accounts import views

def find_user_by_login(login):
     try:
         user = Account.objects.get(login = login)
         return user
     except:
         return None

def find_user_by_id(login):
     try:
         user = Account.objects.get(id = id)
         return user
     except:
         return None

def living_city(id):
    try:
        user = Account.objects.get(pk = id)
        city = City.objects.filter(residents__in = user)
        print(1)
        return city
    except:
        pass


def users(request):
    # context-> list of all Account objects
    context = dict()
    context['users'] = Account.objects.all()
    pass

def user(request, login):
    context = dict()
    account = find_user(login)
    context['account'] = account
    context['living_city'] = living_city(account.id)
    print(context)
    # context -> Account object
    # context -> city preferences

    pass

def login(request):
    context = dict()
    if (request.method == 'POST'):
        login = request.POST['login'] # <input type = "text" name = "login">
        if find_user_by_login(login) != None:
            context['user'] = find_user_by_login(login)
            return render(request, 'app/city/city_search.html', context)
        if find_user_by_login(login) == None:
            return render(request, 'app/account/login.html', context)
    else:
        return render(request, 'app/account/login.html', context)

def register (request):
    context = dict()
    if request.method == 'POST':
        try:
            login_exists = bool(Account.objects.get(login = request.POST['login']))
        except:
            login_exists = False
        try:
            email_exists = bool(Account.objects.get(email = request.POST['email']))
        except:
            email_exists = False
        if login_exists or email_exists:
            return render(request, 'general/register.html', context)
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            login = request.POST['login']
            password = request.POST['password']
            account = Account(name = first_name, surname = last_name, email = email, login = login, password = password, slug = login)
            account.save()
            request.session['user'] = account.pk
            return redirect(reverse(views.login))
    else:
        return render(request, 'general/register.html', context)

def my_account(request):
    context = dict()
    user = Account.object.get(pk = request.session['user'])







# def mainpage(request):
#     context = dict()
#     try:
#         user = Account.objects.get(pk = request.session['user'])
#         context['user'] = user
#     except:
#         context['user'] = None
#         if request.method == 'POST':
#             login_form = LoginForm(request.POST)
#             if login_form.is_valid():
#                 account = Account.objects.get(login = login_form.cleaned_data['username'])
#                 context['pk'] = account.id
#                 request.session['user'] = account.pk
#                 context['user'] = Account.objects.get(pk = request.session['user'])
#                 search_form = SearchForm(request.POST)
#                 context['search_form'] = search_form
#                 return render(request, 'search.html', context)
#         else:
#             login_form = LoginForm(request.POST)
#         context['login_form'] = login_form
#         context['method'] = request.method
#         return render(request, 'login.html', context)
#     if request.method == 'POST':
#         search_form = SearchForm(request.POST)
#         if search_form.is_valid():
#             city = search_form.cleaned_data['city']
#             return redirect(reverse(cityviews.city,args = [city]))
#     else:
#         search_form = SearchForm(request.POST)
#     context['search_form'] = search_form
#     return render(request, 'search.html', context)

# def sign_in(request):
#     context = dict()
#     try:
#         user = Account.objects.get(pk = request.session['user'])
#         context['user'] = user
#     except:
#         context['user'] = None
#     sign_form = SignForm(request.POST)
#     if request.method == 'POST':
#         if sign_form.is_valid():
#             first_name = sign_form.cleaned_data['first_name']
#             last_name = sign_form.cleaned_data['last_name']
#             email = sign_form.cleaned_data['email']
#             username = sign_form.cleaned_data['username']
#             password = sign_form.cleaned_data['password']
#             account = Account(name = first_name, surname = last_name, email = email, login = username, password = password, slug = username)
#             account.save()
#             context['account'] = account
#             request.session['user'] = account.pk
#             return redirect(reverse(views.mainpage))
#     context['sign_form'] = sign_form
#     return render(request, 'sign.html', context)

# def account_page(request, account):
#     context = dict()
#     try:
#         user = Account.objects.get(pk = request.session['user'])
#         context['user'] = user
#     except:
#         pass
#     try:
#         account = Account.objects.get(login = account)
#         context['account'] = account
#     except:
#         pass
#     user_guest = bool(user != account)
#     if user_guest:
#         return render(request, 'account_page.html', context)
#     else:
#         context['recieved_requests'] = FriendRequest.objects.filter(to_user = user)
#         context['sent_requests'] = FriendRequest.objects.filter(from_user = user)
#         context['user'] = user
#         return render(request, 'self_page.html', context)
