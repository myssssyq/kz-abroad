from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('name/<slug:slug>', views.city, name = 'city'),
    path('cities', views.cities, name = 'cities'),
    path('search', views.city_search, name = 'city_search'),
    path('add_city', views.add_city, name = 'add_city')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
