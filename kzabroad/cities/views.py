from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from django.template.defaultfilters import slugify
from .models import City
from accounts.models import *
from django.http import JsonResponse
from cities import views
import accounts.views as accountsviews
import kzabroad.views as mainviews
import wikipedia
import json
import requests

# Create your views here.

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
            for preference in request.POST:
                if preference != 'csrfmiddlewaretoken' and preference != 'checkbox_search':
                    filtering_preference = Prefereneces.objects.get(pk = preference)
                    context['residents'] = context['residents'].filter(prefereneces = filtering_preference)
        return render(request, 'app/city/city_residents.html', context)
    else:
        if request.method == 'POST':
            city.residents.add(user)
            user.living_city = city
            user.save()
            city.save()
            return render(request, 'app/city/city_residents.html', context)
        context['city'] = city
        context['residents'] = city.residents.exclude(login = user.login)
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
    context['cities'] = City.objects.all()
    return render(request, 'app/city/cities.html', context)

def city_search(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(accountsviews.index))
    else:
        pass
    context['user'] = find_user_by_id(request.session['user'])
    context['cities'] = City.objects.all()
    if request.method == 'POST':
        search_city = slugify(request.POST['search'])
        return redirect(reverse(views.city,args = [search_city]))
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
    if request.method == 'POST':
        city = str(request.POST['add'])
        try:
            city_picture = get_wiki_image(str(city) + ' city')
            description = wikipedia.summary(str(city) + ' city')
        except:
            pass
        city_slug = slugify(city)
        city = City(name = city, description = description, picture = city_picture, slug = city_slug)
        city.save()
        return redirect(reverse(views.city,args = [city.name]))
    return render(request, 'app/city/add_city.html', context)



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
