from django.urls import path
from . import views

urlpatterns = [

    path('<slug:city>',views.city, name='city'),
]
