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

def user_validation(func):
    def validation(request, *args, **kwargs):
        try:
            user = Account.objects.get(pk = request.session['user'])
            return func(request, *args, **kwargs)
        except Exception as e:
            context = {'error': e}
            return render(request, '404.html', context = context)
    return validation


def find_user_by_login(login):
     try:
         user = Account.objects.get(login = login)
         return user
     except:
         return None

def find_user_by_email(email):
     try:
         user = Account.objects.get(email = email)
         return user
     except:
         return None

def find_user_by_id(id):
     try:
         user = Account.objects.get(pk = id)
         return user
     except:
         return None

def delete_notification(request):
    notification_list = []
    print('works')
    user = find_user_by_id(request.session['user'])
    for i in request.GET:
        for notification in json.loads(i):
            notification_to_delete = user.notifications.get(id = notification['id'])
            notification_to_delete.delete()
            notification_list.append(int(notification['id']))
    notification_dict = {i:item for i,item in enumerate(notification_list)}
    return JsonResponse(notification_dict)

def delete_friend(request):
    user = Account.objects.get(pk = request.session['user'])
    friend_to_delete = find_user_by_id(request.GET['id'])
    user.friends_list.remove(friend_to_delete)
    user.save()

def friend_request(request):
    notifications_tags = ["Friend request recieved", "Friend request accepted", "Friend request declined"]
    requesting_user = find_user_by_id(request.GET['id'])
    user = Account.objects.get(pk = request.session['user'])
    if request.GET['action'] == "accept":
        friend_request = FriendRequest.objects.get(from_user = requesting_user, to_user = user)
        message = str(user.name) + ' ' + str(user.surname) + ' accepted your friend request.'
        requesting_user.add_notification(notifications_tags[1],message)
        friend_request.delete()
        user.friends_list.add(requesting_user)
    else:
        friend_request = FriendRequest.objects.get(from_user = requesting_user, to_user = user)
        friend_request.delete()
        message = str(user.name) + ' ' + str(user.surname) + ' declined your friend request.'
        requesting_user.add_notification(notifications_tags[2],message)
    return JsonResponse({ "id" : request.GET['id']})

def validate_city(request):
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

def index(request):
    context=dict()
    request.session['user'] = None
    context['user'] = find_user_by_id(request.session['user'])
    return render(request, 'general/index.html', context)

@user_validation
def users(request):
    context = dict()
    context['user'] = user = Account.objects.get(pk = request.session['user'])
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

@user_validation
def user(request, login):
    context = dict()
    notifications_tags = ["Friend request recieved", "Friend request accepted", "Friend request declined"]
    context['user'] = user = Account.objects.get(pk = request.session['user'])
    if find_user_by_login(login) == None:
        raise Http404("Account does not exist")
    else:
        account = find_user_by_login(login)
    context['account'] = account
    context['accounts'] = list(Account.objects.values('name', 'slug', 'surname'))
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
        context['occupations_education'] = {
            "occupation":[
            ]
        }
        context['occupations_work'] = {
            "occupation":[
            ]
        }
        for occupation in account.occupations['occupation']:
            if occupation['class'] == "education":
                context['occupations_education']['occupation'].append(occupation)
            else:
                context['occupations_work']['occupation'].append(occupation)
        context['occupations_work'] = context['occupations_work']['occupation']
        context['occupations_education'] = context['occupations_education']['occupation']
        context['friends'] = account.friends_list.all()
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
            return render(request, 'dist/profile-guest.html', context)
        if request.is_ajax() and 'action' in request.GET:
            try:
                friend_request = FriendRequest.objects.get(to_user = account, from_user = user)
            except:
                friend_request = ''
            if friend_request == '':
                friend_request, created = FriendRequest.objects.get_or_create(to_user = account, from_user = user)
                friend_request.save()
                message = str(user.name) + ' ' + str(user.surname + ' sent you friend request.')
                account.add_notification(notifications_tags[0],message)
                return JsonResponse({"message":"succes"})
            else:
                response = JsonResponse({
                'message': "error"
                })
                response.status_code = 403 # To announce that the user isn't allowed to publish
                return response
        return render(request, 'dist/profile-guest.html', context)
    else:
        try:
            context['message'] = request.session['message']
            del request.session['message']
        except:
            pass
        context['cities'] = City.objects.all()
        context['friends'] = user.friends_list.all()
        context['occupations'] = Occupation.objects.all()
        context['sent_requests'] = FriendRequest.objects.filter(from_user = user)
        context['occupations_education'] = {
            "occupation":[
            ]
        }
        context['occupations_work'] = {
            "occupation":[
            ]
        }
        for occupation in user.occupations['occupation']:
            if occupation['class'] == "education":
                context['occupations_education']['occupation'].append(occupation)
            else:
                context['occupations_work']['occupation'].append(occupation)
        context['occupations_work'] = context['occupations_work']['occupation']
        context['occupations_education'] = context['occupations_education']['occupation']
        context['checked_interests'] = []
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
        return render(request, 'dist/profile-about.html', context)

@user_validation
def user_settings(request, login):
    context = dict()
    context['user'] = user = Account.objects.get(pk = request.session['user'])
    if find_user_by_login(login) == None:
        raise Http404("Account does not exist")
    else:
        account = find_user_by_login(login)
    context['account'] = account
    if request.is_ajax() and 'password' in request.GET:
        user.password = request.GET['password']
        user.save()
        return JsonResponse({
            'message': "succes"
            })
    if request.is_ajax() and 'city_value' in request.GET:
        city_input = request.GET['city_value']
        try:
            city_exists = bool(City.objects.get(name = city_input))
        except:
            city_exists = False
        if city_exists:
            return JsonResponse({
                'message': "succes"
                })
        else:
            response = JsonResponse({
                'message': "error"
                })
            response.status_code = 403 # To announce that the user isn't allowed to publish
            return response
    if request.is_ajax() and 'facebook' in request.POST:
        user.facebook_link = request.POST['facebook']
        user.instagram_link = request.POST['instagram']
        user.twitter_link = request.POST['twitter']
        user.vk_link = request.POST['vk']
        user.tiktok_link = request.POST['tiktok']
        user.save()
    if request.is_ajax() and 'first_name' in request.POST:
        user.name = request.POST['first_name']
        user.surname = request.POST['last_name']
        user.living_city = City.objects.get(name = request.POST['city_input'])
        user.living_city.residents.add(user)
        user.save()
        return JsonResponse({
        "message":"succes"
        })
    if request.method == 'POST' and "add_occupation" in request.POST:
        new_occupation = {
        "class": request.POST['class'],
        "name": request.POST['name'],
        "position": request.POST['position'],
        "description": request.POST['description'],
        "year_from": request.POST['year_from'],
        "year_to": request.POST['year_to']
        }
        user.occupations['occupation'].append(new_occupation)
        user.save()
    if request.method == 'POST' and 'delete_occupation' in request.POST:
        for input in request.POST:
            for iterator in range(len(user.occupations['occupation'])):
                if user.occupations['occupation'][iterator]['name'] == input:
                    user.occupations['occupation'].pop(iterator)
                    break
        user.save()
    if user != account:
        raise Http404("You do not have acces to this page")
    else:
        return render(request, 'dist/options-settings.html', context)

def login(request):
    context = dict()
    context['user'] = find_user_by_id(request.session['user'])
    if (request.method == 'POST'):
        email = request.POST['email']
        if find_user_by_email(email) != None:
            user = find_user_by_email(email)
            if user.password == request.POST['password']:
                context['user'] = user
                request.session['user'] = user.pk
                return redirect(reverse(views.user, args = [user.login]))
            else:
                context['error'] = 'Login or password is incorrect'
                return render(request, 'dist/login.html', context)
        if find_user_by_email(email) == None:
            context['error'] = 'Login or password is incorrect'
            return render(request, 'dist/login.html', context)
    else:
        return render(request, 'dist/login.html', context)

def register (request):
    context = dict()
    context['user'] = find_user_by_id(request.session['user'])
    context['cities'] = City.objects.all()
    if request.is_ajax():
        city_input = request.GET['city_value']
        try:
            city_exists = bool(City.objects.get(name = city_input))
        except:
            city_exists = False
        if city_exists:
            return JsonResponse({
                'message': "succes"
                })
        else:
            response = JsonResponse({
                'message': "error"
                })
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
            occupations = {
                "occupation":[
                ]
            }
            if request.POST['highschool-name'] != "":
                new_occupation = {
                "class": "education",
                "name": request.POST['highschool-name'],
                "position": request.POST['highschool-position'],
                "description": request.POST['highschool-description'],
                "year_from": request.POST['highschool-year_from'],
                "year_to": request.POST['highschool-year_to']
                }
                occupations['occupation'].append(new_occupation)
            if request.POST['university-name'] != "":
                new_occupation = {
                "class": "education",
                "name": request.POST['university-name'],
                "position": request.POST['university-position'],
                "description": request.POST['university-description'],
                "year_from": request.POST['university-year_from'],
                "year_to": request.POST['university-year_to']
                }
                occupations['occupation'].append(new_occupation)
            if request.POST['work-name'] != "":
                new_occupation = {
                "class": "work",
                "name": request.POST['work-name'],
                "position": request.POST['work-position'],
                "description": request.POST['work-description'],
                "year_from": request.POST['work-year_from'],
                "year_to": request.POST['work-year_to']
                }
                occupations['occupation'].append(new_occupation)
            jsonfield = {
            'Interest one': False,
            'Interest two': False,
            'Interest three': False
            }
            try:
                city = City.objects.get(name = request.POST['city_choice'])
                account = Account(name = first_name,
                                  surname = last_name,
                                  email = email,
                                  login = login,
                                  password = password,
                                  slug = login,
                                  living_city = city,
                                  interest = jsonfield,
                                  occupations = occupations)
                account.save()
                city.residents.add(account)
                city.save()
            except:
                account = Account(name = first_name,
                                  surname = last_name,
                                  email = email,
                                  login = login,
                                  password = password,
                                  slug = login,
                                  interest = jsonfield,
                                  occupations = occupations)
            if 'checkbox_highschool_student' in request.POST:
                account.is_highschooler = True
            if 'checkbox_university_student' in request.POST:
                account.is_student = True
            if 'checkbox_worker' in request.POST:
                account.is_worker = True
            account.save()
            request.session['user'] = account.pk
            return redirect(reverse(views.user, args = [account.login]))
    else:
        return render(request, 'dist/signup.html', context)
