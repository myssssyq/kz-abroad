from django.urls import path
from . import views

urlpatterns = [

    path('',views.index, name='index'),
    path('mainpage', views.mainpage, name = 'mainpage'),
    path('sign_in', views.sign_in, name = 'sign_in'),
    path('<slug:account>',views.account_page, name='account_page')
]
