from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .models import City
from accounts.models import *
from django.http import JsonResponse
from cities import views

# Create your views here.

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
         pass
    city = City.objects.get(name = slug)
    if user.living_city == city:
        context['city'] = city
        context['residents'] = city.residents.exclude(login = user.login)
        context['prefereneces'] = Prefereneces.objects.all()
        if request.method == 'POST' and 'request_button' in request.POST:
            requested_user = find_user_by_id(request.POST['resident_id'])
            try:
                friend_request = FriendRequest.objects.get_or_create(to_user = user, from_user = requested_user)
            except:
                friend_request = None
            if not friend_request:
                friend_request = FriendRequest.objects.get_or_create(to_user = requested_user, from_user = user)
                friend_request.save()
        if request.method == 'POST' and 'search_button' in request.POST:
            searching_word = request.POST['search_input']
            context['residents'] = context['residents'].filter(name = searching_word)
        if request.method == 'POST' and 'checkbox_search' in request.POST:
            for preference in request.POST:
                if preference != 'csrfmiddlewaretoken' and preference != 'checkbox_search':
                    filtering_preference = Prefereneces.objects.get(pk = preference)
                    context['residents'] = context['residents'].filter(prefereneces = filtering_preference)
            #print(list(dict(request.POST).items()))
        return render(request, 'app/city/city_residents.html', context)
    else:
        if request.method == 'POST':
            city.residents.add(user)
            user.living_city = city
            user.save()
            city.save()
        context['city'] = city
        context['residents'] = city.residents.exclude(login = user.login)
        return render(request, 'app/city/city_nonresidents.html', context)


def cities(request):
    context = dict()
    context['cities'] = City.objects.all()
    return render(request, 'app/city/cities.html', context)

def city_search(request):
    context = dict()
    context['user'] = find_user_by_id(request.session['user'])
    if request.method == 'POST':
        search_city = request.POST['search']
        return redirect(reverse(views.city,args = [search_city]))
    return render(request, 'app/city/city_search.html', context)





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
