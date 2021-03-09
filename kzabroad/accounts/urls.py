from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'), #login
    path('register', views.register, name = 'register'), #register
    path('user/<slug:login>', views.user, name = 'user'), #user
    path('users', views.users, name = 'users') #users
    #landing

#    path('',views.index, name='index'),
#    path('mainpage', views.mainpage, name = 'mainpage'),
#    path('sign_in', views.sign_in, name = 'sign_in'),
#    path('<slug:account>',views.account_page, name='account_page')
]
