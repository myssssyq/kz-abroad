from django.shortcuts import render
from .models import City
from accounts.models import *
from django.http import JsonResponse

# Create your views here.

def city(request, slug):
    # context -> city Object
    pass


def cities(request):
    #all cities
    pass





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
