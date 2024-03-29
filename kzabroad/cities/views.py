from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from django.template.defaultfilters import slugify
from django.contrib.postgres.search import TrigramSimilarity
from .models import City
from accounts.models import *
from django.http import JsonResponse
from cities import views
import accounts.views as accountsviews
import kzabroad.views as mainviews
import wikipedia
import json
import requests
from django.db import connection
from geopy.geocoders import Nominatim

with connection.cursor() as cursor:
    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
geolocator = Nominatim(user_agent="cities")

# Create your views here.
#geolocator = Nominatim(user_agent="cities")
#location = geolocator.geocode("Paris")
#print((location.latitude, location.longitude))

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except:
        return 0

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

def city(request, slug):
    # context -> city Object
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    try:
        city = City.objects.get(slug = slug)
    except:
        request.session['message'] = "Sorry, this city doesn't exist. Do you want to add city to database?"
        return redirect(reverse(views.add_city))
        #raise Http404("City does not exist")
    try:
        context['city_description'] = city.description
        context['city_image'] = city.picture
    except:
        pass
    if user.living_city == city:
        context['city'] = city
        context['residents'] = city.residents.exclude(login = user.login)
        context['prefereneces'] = Prefereneces.objects.all()
        context['need_a_guide'] = True
        try:
            if city.guide_session.get(requesting_user = user):
                context['need_a_guide'] = False
        except:
            pass
        if request.method == 'POST' and 'request_button' in request.POST:
            requested_user = find_user_by_id(request.POST['resident_id'])
            try:
                friend_request = FriendRequest.objects.get(to_user = user, from_user = requested_user)
            except:
                friend_request = None
            if not friend_request:
                friend_request, created = FriendRequest.objects.get_or_create(to_user = requested_user, from_user = user)
                friend_request.save()
            return render(request, 'app/city/city_residents.html', context)
        if request.method == 'POST' and 'search_button' in request.POST:
            searching_word = request.POST['search_input']
            context['residents'] = context['residents'].filter(name = searching_word)
        if request.method == 'POST' and 'checkbox_search' in request.POST:
            for interest_iterable in user.interest:
                if interest_iterable in request.POST.getlist('checks'):
                    context['residents'] = context['residents'].filter(interest__contains = {interest_iterable: True} )
        return render(request, 'app/city/city_residents.html', context)
    else:
        context['city'] = city
        context['residents'] = city.residents.exclude(login = user.login)[:5]
        return render(request, 'app/city/city_nonresidents.html', context)

def cities(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    if request.method == 'POST':
        searching_city = City.objects.annotate(similarity=TrigramSimilarity('name', request.POST['search']),).filter(similarity__gt=0.6).order_by('-similarity')
        context['cities'] = searching_city
        return render(request, 'app/city/cities1.html', context)
    context['cities'] = City.objects.all().order_by('name')
    return render(request, 'app/city/cities1.html', context)

def city_search(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    context['cities'] = City.objects.all()
    if request.method == 'POST':
        search_city = slugify(request.POST['search'])
        try:
            city_exists = bool(City.objects.get(slug = search_city))
        except:
            city_exists = False
        if city_exists:
            return redirect(reverse(views.city,args = [search_city]))
        else:
            return redirect(reverse(views.search_results,args = [search_city]))
    return render(request, 'app/city/city_search.html', context)

def add_city(request):
    context = dict()
    try:
        context['message'] = request.session['message']
        del request.session['message']
    except:
        pass
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    if request.is_ajax():
        try:
            city_exists = bool(City.objects.get(name = request.POST['add']))
        except:
            city_exists = False
        if not city_exists:
            return JsonResponse({
                'message': 'success'
                })
        else:
            response = JsonResponse({"message": "error"})
            response.status_code = 403 # To announce that the user isn't allowed to publish
            return response
    if request.method == 'POST':
        city = str(request.POST['add'])
        try:
            city_picture = get_wiki_image(str(city) + ' city')
            description = wikipedia.summary(str(city) + ' city')
        except:
            pass
        try:
            city_page = wikipedia.page(str(city) + ' city')
            url = city_page.url
        except:
            pass
        try:
            location = geolocator.geocode(str(city))
            city_latitude = location.latitude
            city_longtitude = location.longitude
        except:
            city_latitude = None
            city_longtitude = None
        try:
            city_request = RequestToCreateCity(city_name = city, wiki_link = url, requesting_user = user, description = description, picture = city_picture, latitude = city_latitude, longitude = city_longtitude)
            city_request.save()
            request_failed = False
        except:
            try:
                city_request = RequestToCreateCity(city_name = city, requesting_user = user, description = description, picture = city_picture, latitude = city_latitude, longitude = city_longtitude)
                city_request.save()
                request_failed = False
            except:
                request_failed = True
        #city_slug = slugify(city)
        #city = City(name = city, description = description, picture = city_picture, slug = city_slug)
        #city.save()
        if request_failed:
            request.session['message'] = "Sorry, we couldn't find this city"
            return redirect(reverse(views.add_city))
        request.session['message'] = "City was successfuly added."
        return redirect(reverse(views.add_city))
    return render(request, 'app/city/add_city.html', context)

def city_requests(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    if not user.is_admin:
        # TODO:
        request.session['message'] = "You do not have permission to visit that page."
        return redirect(reverse(accountsviews.user, args = [user.login]))
    else:
        context['requests'] = RequestToCreateCity.objects.all()
        notifications_tags = ["Your city request was accepted", "Your city request was declined"]
        if request.method == 'POST' and 'accept' in request.POST:
            requested_city = RequestToCreateCity.objects.get(city_name = request.POST['request_input'])
            slug = slugify(requested_city.city_name)
            city = City(name = requested_city.city_name, slug = slug, description = requested_city.description, picture = requested_city.picture, latitude = requested_city.latitude, longitude = requested_city.longitude)
            city.save()
            requesting_user = requested_city.requesting_user
            message = 'Your request to add city named ' + str(city.name) + ' was accepted'
            requesting_user.add_notification(notifications_tags[0],message)
            requested_city.delete()
        if request.method == 'POST' and 'decline' in request.POST:
            requested_city = RequestToCreateCity.objects.get(city_name = request.POST['request_input'])
            requesting_user = requested_city.requesting_user
            message = 'Your request to add city named ' + str(requested_city.city_name) + ' was declined'
            requesting_user.add_notification(notifications_tags[1],message)
            requested_city.delete()
        return render(request, 'app/city/city_creation_requests.html', context)

def search_results(request, slug):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    try:
        results = City.objects.annotate(similarity=TrigramSimilarity('name', slug),).filter(similarity__gt=0).order_by('-similarity')
        context['results_similar'] = results
        matching_cities = results.values('name')
        other_cities = City.objects.exclude(name__in = matching_cities)
        context['other_cities'] = other_cities
    except:
        pass
    return render(request, 'app/city/search_results.html', context)


# def city(request, city):
#     context = dict()
#     try:
#         user = Account.objects.get(pk = request.session['user'])
#         context['user'] = user
#     except:
#         pass
#     city = City.objects.get(name = city)
#     if not city.livesin(user):
#         if request.is_ajax():
#             city.residents.add(user)
#             return JsonResponse({
#                 'message': 'success'
#                 })
#         residents = city.residents.exclude(login = user.login)
#         context['residents'] = residents
#         context['city'] = city
#         return render(request, 'city1.html', context)
#     else:
#         if request.is_ajax():
#             try:
#                 request_user = Account.objects.get(id = request.POST['request_input'])
#             except:
#                 pass
#             try:
#                 friend_request = FriendRequest(to_user = request_user, from_user = user)
#                 friend_request.save()
#             except:
#                 pass
#             residents = city.residents.exclude(login = user.login)
#             context['residents'] = residents
#             context['city'] = city
#             return JsonResponse({
#                 'message': 'success'
#                 })
#         residents = city.residents.exclude(login = user.login)
#         context['residents'] = residents
#         context['city'] = city
#         return render(request, 'city2.html', context)
