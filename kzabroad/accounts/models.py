from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from .models import *
from cities.models import *
from django.utils.timezone import now

GENDER = (

    ("Male", "Male"),
    ("Female", "Female")

)

TAGS = (

    ("Your city request was accepted", "Accepted_city_request"),
    ("Your city request was declined", "Declined_city_request"),
    ("Friend request recieved", "Received_friend_request"),
    ("Friend request accepted", "Accepted_friend_request"),
    ("Friend request declined", "Declined_friend_request")

)


class Account(models.Model):
    #<----------------------------Registration Field Begin---------------------------->
    id = models.AutoField(primary_key=True, editable=True)
    login = models.CharField(max_length = 30, unique = True)
    email = models.EmailField(max_length = 255, unique = True, blank = True)
    password = models.CharField(max_length = 30)
    slug = models.SlugField(max_length=200, default = None)
    #<----------------------------Registration Field END---------------------------->


    #<----------------------------About BEGIN---------------------------->
    name = models.CharField(max_length = 30, blank = True)
    surname = models.CharField(max_length = 30, blank = True)
    about = models.TextField(blank = True)
    gender = models.CharField(choices = GENDER, max_length = 6, blank = True)
    age = models.IntegerField(blank = True, null = True)
    created = models.DateTimeField(default=now, editable=True)
    occupations = models.JSONField(default = None, blank = True)
    #occupation = models.ForeignKey('Occupation', related_name = 'occupation', on_delete=models.SET_NULL, null = True, blank = True)
    #<----------------------------About END---------------------------->

    #<----------------------------Links BEGIN---------------------------->
    instagram_link = models.CharField(max_length = 40, blank = True)
    tiktok_link = models.CharField(max_length = 40, blank = True)
    vk_link = models.CharField(max_length = 40, blank = True)
    facebook_link = models.CharField(max_length = 40, blank = True)
    twitter_link = models.CharField(max_length = 40, blank = True)
    #<----------------------------Links END---------------------------->

    #<----------------------------Friends BEGIN---------------------------->

    friends_list = models.ManyToManyField("self", blank=True)

    #<----------------------------Friends END---------------------------->

    #<----------------------------City BEGIN---------------------------->

    living_city = models.ForeignKey('cities.City', related_name = 'city', on_delete=models.SET_NULL, null = True, blank = True)
    is_guide = models.BooleanField(default = False, blank = True)
    cost_preference = models.CharField(max_length = 10, default = None, blank = True, null = True)
    prefereneces = models.ManyToManyField('Prefereneces', blank = True)

    #<----------------------------City END---------------------------->

    #<----------------------------Role BEGIN---------------------------->

    is_admin = models.BooleanField(default = False, blank = True)
    is_highschooler = models.BooleanField(default = False, blank = True)
    is_student = models.BooleanField(default = False, blank = True)
    is_worker = models.BooleanField(default = False, blank = True)

    #<----------------------------Role END---------------------------->

    #<----------------------------Interests BEGIN---------------------------->

    #interest = ArrayField(models.CharField(max_length=50, blank=True), size=8, default = None, blank = True)
    interest = models.JSONField(default = None, blank = True)

    #<----------------------------Interests END---------------------------->

    #<----------------------------Notification BEGIN---------------------------->

    notifications = models.ManyToManyField('Notification', blank = True)

    #<----------------------------Notification END---------------------------->

    def add_notification(self, tag, message):
        notification = Notification(tag = tag, message = message, to_user = self)
        notification.save()
        self.notifications.add(notification)

    def __str__(self):
        return (str(self.name) + ' ' + str(self.surname) + ' (' + str(self.id) + ')')


class FriendRequest(models.Model):
    to_user = models.ForeignKey("Account", related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey("Account", related_name='from_user', on_delete=models.CASCADE)

    def __str__(self):
	       return ('From ' + str(self.from_user) + ' to ' + str(self.to_user))

class Prefereneces(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    name = models.CharField(max_length=200, blank = True)
    def __str__(self):
        return ('(' + str(self.id) + ') : ' + str(self.name))

class Occupation(models.Model):
    sectors = (
        ("Highschool", "Highschool"),
        ("University", "University"),
        ("Working place", "Working place")
    )
    name = models.CharField(max_length = 128, blank = True)
    sector = models.CharField(choices = sectors, max_length = 64, blank = True)
    related_people = models.ManyToManyField('Account', related_name = 'amount_of_people', blank = True)
    city = models.ForeignKey('cities.City', related_name ='occupation_city', on_delete=models.SET_NULL, null = True)
    def __str__(self):
        #return (str(self.sector) + ': ' + str(self.name))
        return(str(self.name))

class Notification(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    tag = models.CharField(choices = TAGS, max_length = 50, blank = True)
    message = models.TextField(blank = True)
    to_user = models.ForeignKey("Account", related_name='notification_to_user', on_delete=models.CASCADE, null = True)

    def checkboxed(self):
        return("checkbox-" + str(self.id))

    def __str__(self):
        return('(' + str(self.id) +')' + str(self.tag) + ': ' + str(self.to_user.login))
