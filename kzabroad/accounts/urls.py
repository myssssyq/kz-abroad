from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('user/<slug:login>', views.user, name = 'user'),
    path('user/<slug:login>/settings', views.user_settings, name = 'user_settings'),
    path('users', views.users, name = 'users'),
    path('notifications', views.notifications, name = 'notifications')

#    path('',views.index, name='index'),
#    path('mainpage', views.mainpage, name = 'mainpage'),
#    path('sign_in', views.sign_in, name = 'sign_in'),
#    path('<slug:account>',views.account_page, name='account_page')
]
