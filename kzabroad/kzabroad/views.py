from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import *
import accounts.views as views


def find_user_by_id(id):
     try:
         user = Account.objects.get(pk = id)
         return user
     except:
         return None

def about(request):
    context=dict()
    request.session['user'] = None
    return render(request, 'base.html', context)

def error404(request, exception):
    context = dict()
    return render(request, '404.html', context)

def main_page(request):
    context = dict()
    try:
        user = Account.objects.get(pk = request.session['user'])
        context['user'] = user
    except:
        return redirect(reverse(views.index))
    else:
        pass
    return render(request, 'general/main_page.html', context)
