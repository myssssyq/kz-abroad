from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.postgres.search import TrigramSimilarity
from django.http import Http404
from .forms import *
from .models import *
import cities.views as cityviews
from accounts import views
from django.http import JsonResponse
import json
from fuzzywuzzy import process
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')

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
    return render(request, 'general/landing_page.html', context)

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
    if find_user_by_login(login) == None:
        raise Http404("Account does not exist")
    else:
        account = find_user_by_login(login)
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
                account.add_notification(notifications_tags[0],message)
            context['request_exists'] = True
            return render(request, 'app/account/user.html', context)
        return render(request, 'app/account/user.html', context)
    else:
        try:
            context['message'] = request.session['message']
            del request.session['message']
        except:
            pass
        context['cities'] = City.objects.all()
        context['friends'] = user.friends_list.all()
        context['occupations'] = Occupation.objects.all()
        context['recieved_requests'] = FriendRequest.objects.filter(to_user = user)
        context['sent_requests'] = FriendRequest.objects.filter(from_user = user)
        context['checked_interests'] = []
        for interest in user.interest:
            if user.interest[str(interest)]:
                context['checked_interests'].append(interest)
        if request.is_ajax() and 'occupation_value' in request.GET:
            occupation_input = request.GET['occupation_value']
            try:
                occupation_exists = bool(Occupation.objects.get(name = occupation_input))
            except:
                occupation_exists = False
            if not occupation_exists:
                results = Occupation.objects.annotate(similarity=TrigramSimilarity('name', occupation_input),).filter(similarity__gt=0.55).order_by('-similarity')
                context['results_similar'] = results
                matching_occupations = results.values('name')
                if results:
                    return JsonResponse({
                        'message': str(results[0]),
                        })
        if request.is_ajax() and 'city_value' in request.GET:
            city_input = request.GET['city_value']
            try:
                city_exists = bool(City.objects.get(name = city_input))
            except:
                city_exists = False
            if not city_exists:
                results = City.objects.annotate(similarity=TrigramSimilarity('name', city_input),).filter(similarity__gt=0.55).order_by('-similarity')
                context['results_similar'] = results
                #matching_cites = results.values('name')
                if results:
                    return JsonResponse({
                        'message': str(results[0]),
                        })
        if request.is_ajax() and request.method == 'POST':
            if 'city_choice' in request.POST:
                if request.POST['city_choice'] != '':
                    try:
                        city_exists = bool(City.objects.get(name = request.POST['city_choice']))
                    except:
                        city_exists = False
                    if city_exists:
                        return JsonResponse({
                            'message': 'success'
                            })
                    else:
                        response = JsonResponse({
                        'city_exists': str(city_exists)
                        })
                        response.status_code = 403 # To announce that the user isn't allowed to publish
                        return response
                else:
                    return JsonResponse({
                        'message': 'success'
                        })
        if request.method == 'POST'  and 'name' in request.POST:
            user.name = request.POST['name']
            user.surname = request.POST['surname']
            user.email = request.POST['email']
            user.password = request.POST['password']
            user.tiktok_link = request.POST['tiktok']
            user.vk_link = request.POST['vk']
            user.instagram_link = request.POST['instagram']
            user.facebook_link = request.POST['facebook']
            user.twitter_link = request.POST['twitter']
            if 'is_highschooler' in request.POST:
                user.is_highschooler = True
            else:
                user.is_highschooler = False
            if 'is_student' in request.POST:
                user.is_student = True
            else:
                user.is_student = False
            if 'is_worker' in request.POST:
                user.is_worker = True
            else:
                user.is_worker = False
            if 'occupation_choice' in request.POST:
                if request.POST['occupation_choice'] != '':
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
                else:
                    user.occupation = None
            if 'city_choice' in request.POST:
                if request.POST['city_choice'] != '':
                    user_living_city = City.objects.get(name = request.POST['city_choice'])
                    try:
                        user.living_city.residents.remove(user)
                        user.living_city.save()
                    except:
                        pass
                    user.living_city = user_living_city
                    user_living_city.residents.add(user)
                    user_living_city.save()
                else:
                    user.living_city = None
                    user.occupation = None
            if 'no' in request.POST:
                user.is_guide = False
                try:
                    user.living_city.guides.remove(user)
                except:
                    pass
            if 'yes' in request.POST:
                user.is_guide = True
                user.living_city.guides.add(user)
            if 'checks' in request.POST:
                interests_list = request.POST.getlist('checks')
                for interest in user.interest:
                    if interest in interests_list:
                        user.interest[str(interest)] = True
                    else:
                        user.interest[str(interest)] = False
            user.save()
            try:
                user.living_city.save()
            except:
                pass
            return redirect(reverse(views.user, args = [user.login]))
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
        if request.method == 'POST' and 'delete_friend' in request.POST:
            friend_to_delete = find_user_by_id(request.POST['delete_input'])
            user.friends_list.remove(friend_to_delete)
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
        if request.POST['city_choice'] != "":
            try:
                city_exists = bool(City.objects.get(name = request.POST['city_choice']))
            except:
                city_exists = False
            if city_exists:
                return JsonResponse({
                    'message': 'success'
                    })
            else:
                response = JsonResponse({
                "message": "there was an error"
                })
                response.status_code = 403 # To announce that the user isn't allowed to publish
                return response
        else:
            return JsonResponse({
                'message': 'success'
                })
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
            jsonfield = {
            'Interest one': False,
            'Interest two': False,
            'Interest three': False
            }
            try:
                city = City.objects.get(name = request.POST['city_choice'])
                account = Account(name = first_name, surname = last_name, email = email, login = login, password = password, slug = login, living_city = city, interest = jsonfield)
                account.save()
            except:
                account = Account(name = first_name, surname = last_name, email = email, login = login, password = password, slug = login, interest = jsonfield)
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
    if request.method == "POST":
        for notification in user.notifications.all():
            notification.delete()
            return redirect(reverse(views.notifications))
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
