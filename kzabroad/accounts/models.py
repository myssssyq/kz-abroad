from django.db import models
from .models import *
from cities.models import *

GENDER = (

    ("Male", "Male"),
    ("Female", "Female")

)

class Account(models.Model):
    #<----------------------------Registration Field Begin---------------------------->
    id = models.AutoField(primary_key=True, editable=True)
    login = models.CharField(max_length = 30, unique = True)
    email = models.EmailField(max_length = 30, unique = True, blank = True)
    password = models.CharField(max_length = 30)
    slug = models.SlugField(max_length=200, default = None)
    #<----------------------------Registration Field END---------------------------->


    #<----------------------------Personality BEGIN---------------------------->
    name = models.CharField(max_length = 30, blank = True)
    surname = models.CharField(max_length = 30, blank = True)
    about = models.TextField(blank = True)
    gender = models.CharField(choices = GENDER, max_length = 6, blank = True)
    is_guide = models.BooleanField(default = False, blank = True)
    age = models.IntegerField(blank = True, null = True)
    cost_preference = models.CharField(max_length = 10, default = None, blank = True, null = True)
    #<----------------------------Personality END---------------------------->

    #<----------------------------Friends BEGIN---------------------------->

    friends_list = models.ManyToManyField("self", blank=True)

    #<----------------------------Friends END---------------------------->

    #<----------------------------City BEGIN---------------------------->

    living_city = models.ForeignKey('cities.City', related_name = 'city', on_delete=models.CASCADE, null = True)

    #<----------------------------City END---------------------------->


    def __str__(self):
        return (str(self.name) + ' ' + str(self.surname) + ' (' + str(self.id) + ')')


class FriendRequest(models.Model):
    to_user = models.ForeignKey("Account", related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey("Account", related_name='from_user', on_delete=models.CASCADE)

    def inbox(self,user):
        return self.objects.filter(to_user = user)

    def __str__(self):
	       return ('From ' + str(self.from_user) + ' to ' + str(self.to_user))
