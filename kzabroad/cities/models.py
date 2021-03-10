from django.db import models
from accounts.models import *
from django.utils.timezone import now

STATUS = (

    ("Waiting", "Waiting"),
    ("Needs approve", "Needs approve"),
    ("In process", "In process"),
    ("Finished", "Finished")

)

class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, default = None)
    residents = models.ManyToManyField('accounts.Account', related_name = 'residents')
    guides = models.ManyToManyField('accounts.Account', related_name = 'guides')
    description = models.TextField()
    picture = models.CharField(max_length=200)

    def __str__(self):
        return (str(self.name))
