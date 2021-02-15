from django.shortcuts import render
from django.shortcuts import redirect

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
    return render(request, 'base.html', context)

def about(request):
    context=dict()
    request.session['user'] = None
    return render(request, 'base.html', context)

def error404(request, exception):
    context = dict()
    return render(request, '404.html', context)
