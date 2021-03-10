from django.db import models
from accounts.models import *
from django.utils.timezone import now

class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, default = None)
    residents = models.ManyToManyField('accounts.Account', related_name = 'residents')
    guides = models.ManyToManyField('accounts.Account', related_name = 'guides')
    description = models.TextField()
    picture = models.CharField(max_length=200)

    def __str__(self):
        return (str(self.name))

class RequestToCreateCity(models.Model):
    city_name = models.CharField(max_length=200, unique=True)
    wiki_link = models.CharField(max_length=200, unique=True)
    requesting_user = models.ForeignKey('accounts.Account', related_name = 'requesting_user', on_delete=models.CASCADE, null = True)
    description = models.TextField()
    picture = models.CharField(max_length=200)

    def __str__(self):
        return (str(self.city_name))
