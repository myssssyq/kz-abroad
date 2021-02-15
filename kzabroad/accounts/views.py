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

def find_user_by_id(id):
     try:
         user = Account.objects.get(pk = id)
         return user
     except:
         return None

def index(request):
    context=dict()
    request.session['user'] = None
    context['user'] = find_user_by_id(request.session['user'])
    return render(request, 'general/index.html', context)

def users(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(views.index))
    else:
        pass
    context['users'] = Account.objects.all()
    return render(request, 'app/account/users.html', context)

def user(request, login):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(views.index))
    else:
        pass
    try:
        account = find_user_by_login(login)
    except:
        raise Http404("Account does not exist")
    context['account'] = account
    if user != account:
        return render(request, 'app/account/user.html', context)
    else:
        if user.is_guide:
            context['recieved_guide_requests'] = user.living_city.guide_session.filter(guide = None)
        else:
            try:
                not_approved_request = user.living_city.guide_session.get(status = "Needs approve", requesting_user = user)
                context['not_approved_request'] = not_approved_request
            except:
                context['not_approved_request'] = None
        context['recieved_requests'] = FriendRequest.objects.filter(to_user = user)
        context['sent_requests'] = FriendRequest.objects.filter(from_user = user)
        if request.method == 'POST' and 'change_form' in request.POST:
            user.name = request.POST['name']
            user.surname = request.POST['surname']
            user.email = request.POST['email']
            user.password = request.POST['password']
            if 'no' in request.POST:
                user.is_guide = False
                try:
                    user.living_city.guides.remove(user)
                except:
                    pass
            if 'yes' in request.POST:
                user.is_guide = True
                user.living_city.guides.add(user)
            user.save()
            try:
                user.living_city.save()
            except:
                pass
            return render(request, 'app/account/my_account.html', context)
        if request.method == 'POST' and 'accept' in request.POST:
            requesting_user = find_user_by_id(request.POST['request_input'])
            friend_request = FriendRequest.objects.get(from_user = requesting_user)
            friend_request.delete()
            user.friends_list.add(requesting_user)
        if request.method == 'POST' and 'decline' in request.POST:
            requesting_user = find_user_by_id(request.POST['request_input'])
            friend_request = FriendRequest.objects.get(from_user = requesting_user)
            friend_request.delete()
        if request.method == 'POST' and 'approve_accept' in request.POST:
            not_approved_request.status = 'In procces'
            not_approved_request.save()
        if request.method == 'POST' and 'approve_decline' in request.POST:
            not_approved_request.status = 'Waiting'
            not_approved_request.guide = None
            not_approved_request.save()
        if request.method == 'POST' and 'guide_accept' in request.POST:
            requesting_user = find_user_by_id(request.POST['request_input'])
            guide_session = user.living_city.guide_session.get(requesting_user = requesting_user)
            guide_session.guide = user
            guide_session.status = 'Needs approve'
            guide_session.save()
        return render(request, 'app/account/my_account.html', context)

def login(request):
    context = dict()
    context['user'] = find_user_by_id(request.session['user'])
    if (request.method == 'POST'):
        login = request.POST['login'] # <input type = "text" name = "login">
        if find_user_by_login(login) != None:
            user = find_user_by_login(login)
            if user.password == request.POST['password']:
                context['user'] = user
                request.session['user'] = user.pk
                return redirect(reverse(views.user, args = [user.login]))
            else:
                context['error'] = 'Login or password is incorrect'
                return render(request, 'app/account/login.html', context)
        if find_user_by_login(login) == None:
            context['error'] = 'Login or password is incorrect'
            return render(request, 'app/account/login.html', context)
    else:
        return render(request, 'app/account/login.html', context)

def register (request):
    context = dict()
    context['user'] = find_user_by_id(request.session['user'])
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
            return redirect(reverse(views.user, args = [account.login]))
    else:
        return render(request, 'general/register.html', context)






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
