from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .forms import *
from .models import *
import cities.views as cityviews
from accounts import views

def index(request):
    context=dict()
    request.session['user'] = None
    return render(request, 'base.html', context)

def mainpage(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        context['user'] = None
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                account = Account.objects.get(login = login_form.cleaned_data['username'])
                context['pk'] = account.id
                request.session['user'] = account.pk
                context['user'] = Account.objects.get(pk = request.session['user'])
                search_form = SearchForm(request.POST)
                context['search_form'] = search_form
                return render(request, 'search.html', context)
        else:
            login_form = LoginForm(request.POST)
        context['login_form'] = login_form
        context['method'] = request.method
        return render(request, 'login.html', context)
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            city = search_form.cleaned_data['city']
            return redirect(reverse(cityviews.city,args = [city]))
    else:
        search_form = SearchForm(request.POST)
    context['search_form'] = search_form
    return render(request, 'search.html', context)

def sign_in(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        context['user'] = None
    sign_form = SignForm(request.POST)
    if request.method == 'POST':
        if sign_form.is_valid():
            first_name = sign_form.cleaned_data['first_name']
            last_name = sign_form.cleaned_data['last_name']
            email = sign_form.cleaned_data['email']
            username = sign_form.cleaned_data['username']
            password = sign_form.cleaned_data['password']
            account = Account(name = first_name, surname = last_name, email = email, login = username, password = password, slug = username)
            account.save()
            context['account'] = account
            request.session['user'] = account.pk
            return redirect(reverse(views.mainpage))
    context['sign_form'] = sign_form
    return render(request, 'sign.html', context)

def account_page(request, account):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        pass
    try:
        account = Account.objects.get(login = account)
        context['account'] = account
    except:
        pass
    user_guest = bool(user != account)
    if user_guest:
        return render(request, 'account_page.html', context)
    else:
        context['recieved_requests'] = FriendRequest.objects.filter(to_user = user)
        context['sent_requests'] = FriendRequest.objects.filter(from_user = user)
        context['user'] = user
        return render(request, 'self_page.html', context)
