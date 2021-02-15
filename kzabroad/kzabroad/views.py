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

def error404(request, *args):
    # 2. Generate Content for this view
    template = loader.get_template('404.html')
    context = dict()
    # 3. Return Template for this view + Data
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)
