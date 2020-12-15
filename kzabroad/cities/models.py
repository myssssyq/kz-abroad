from django.db import models
from accounts.models import *

class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, default = None)
    residents = models.ManyToManyField('accounts.Account')
    description = models.TextField()
    picture = models.ImageField(upload_to = "images/", blank=True)

    def __str__(self):
        return (str(self.name))

    def livesin(self, user):
        if user in self.residents.all():
            return True
