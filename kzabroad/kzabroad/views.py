from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    context=dict()
    request.session['user'] = None
    return render(request, 'base.html', context)

def about(request):
    context=dict()
    request.session['user'] = None
    return render(request, 'base.html', context)

    
