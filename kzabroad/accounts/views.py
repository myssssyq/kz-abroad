from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .forms import *
from .models import *
import cities.views as cityviews
from accounts import views
from django.http import JsonResponse
import json
from fuzzywuzzy import process

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
    users = Account.objects.all()
    context['cities'] = City.objects.all()
    context['occupations'] = Occupation.objects.all()
    if request.method == 'POST':
        try:
            form_living_city = City.objects.get(name = request.POST['form_living_city'])
        except:
            form_living_city = None
        try:
            form_occupation = Occupation.objects.get(name = request.POST['form_occupation'])
        except:
            form_occupation = None
        if form_living_city != None:
            users = users.filter(living_city = form_living_city)
        if form_occupation != None:
            users = users.filter(occupation = form_occupation)
    context['users'] = users
    return render(request, 'app/account/users.html', context)

def user(request, login):
    context = dict()
    notifications_tags = ["Friend request recieved", "Friend request accepted", "Friend request declined"]
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
        are_friends = user.friends_list.filter(login = account.login).exists()
        context['are_friends'] = are_friends
        try:
            sent_request_from_user = FriendRequest.objects.get(to_user = account, from_user = user)
        except:
            sent_request_from_user = False
        try:
            friend_request = FriendRequest.objects.get(to_user = user, from_user = account)
        except:
            friend_request = False
        if sent_request_from_user or friend_request or are_friends:
            context['request_exists'] = True
        else:
            context['request_exists'] = False
        context['is_guide'] = account.is_guide
        if request.method == 'POST':
            try:
                friend_request = FriendRequest.objects.get(to_user = user, from_user = account)
            except:
                friend_request = None
            if not friend_request:
                friend_request, created = FriendRequest.objects.get_or_create(to_user = account, from_user = user)
                friend_request.save()
                message = str(user.name) + ' ' + str(user.surname + ' sent you friend request.')
                requesting_user.add_notification(notifications_tags[0],message)
            context['request_exists'] = True
            return render(request, 'app/account/user.html', context)
        return render(request, 'app/account/user.html', context)
    else:
        context['occupations'] = Occupation.objects.all()
        context['recieved_requests'] = FriendRequest.objects.filter(to_user = user)
        context['sent_requests'] = FriendRequest.objects.filter(from_user = user)
        if request.method == 'POST' and 'change_form' in request.POST:
            user.name = request.POST['name']
            user.surname = request.POST['surname']
            user.email = request.POST['email']
            user.password = request.POST['password']
            user.tiktok_link = request.POST['tiktok']
            user.vk_link = request.POST['vk']
            user.instagram_link = request.POST['instagram']
            user.facebook_link = request.POST['facebook']
            user.twitter_link = request.POST['twitter']
            if 'occupation_choice' in request.POST:
                occupation_list = Occupation.objects.filter(city = user.living_city)
                occupation_list = occupation_list.values_list('name')
                occupation_match = (process.extract(request.POST['occupation_choice'], occupation_list, limit = 1))[0]
                occupation_name = occupation_match[0][0]
                occupation_match_score = occupation_match[1]
                if occupation_match_score >= 90:
                    user.occupation = Occupation.objects.get(name = occupation_name)
                else:
                    new_occupation = Occupation(name = request.POST['occupation_choice'], city = user.living_city)
                    new_occupation.save()
                    user.occupation = new_occupation
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
            friend_request = FriendRequest.objects.get(from_user = requesting_user, to_user = user)
            message = str(user.name) + ' ' + str(user.surname) + ' accepted your friend request.'
            requesting_user.add_notification(notifications_tags[1],message)
            friend_request.delete()
            user.friends_list.add(requesting_user)
        if request.method == 'POST' and 'decline' in request.POST:
            requesting_user = find_user_by_id(request.POST['request_input'])
            friend_request = FriendRequest.objects.get(from_user = requesting_user, to_user = user)
            friend_request.delete()
            message = str(user.name) + ' ' + str(user.surname) + ' declined your friend request.'
            requesting_user.add_notification(notifications_tags[2],message)
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
    context['cities'] = City.objects.all()
    if request.is_ajax():
        try:
            city_exists = bool(City.objects.get(name = request.POST['city_choice']))
        except:
            city_exists = False
        if city_exists:
            return JsonResponse({
                'message': 'success'
                })
        else:
            response = JsonResponse({"message": "there was an error"})
            response.status_code = 403 # To announce that the user isn't allowed to publish
            return response
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

def notifications(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(views.index))
    else:
        pass
    context['notifications'] = user.notifications.all()
    for notification in context['notifications']:
        notification.delete()
    return render(request, 'app/account/notifications.html', context)



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
