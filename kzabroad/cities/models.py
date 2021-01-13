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
    guide_session = models.ManyToManyField('GuideSession', related_name = 'guide_session', blank = True)
    picture = models.ImageField(upload_to = "images/", blank=True)

    def __str__(self):
        return (str(self.name))

class GuideSession(models.Model):
    status = models.CharField(choices = STATUS, max_length = 15, blank = True)
    requesting_user = models.ForeignKey('accounts.Account', related_name='requesting_user', on_delete=models.CASCADE)
    guide = models.ForeignKey('accounts.Account', related_name='guide', on_delete=models.CASCADE, blank = True, null = True)
    created = models.DateTimeField(default=now, editable=True)

    def __str__(self):
        try:
            guide_name = self.guide.login
        except:
            guide_name = 'Not assigned'
        return('Guide: ' + str(guide_name) + '; Requesting user: ' + str(self.requesting_user.login) + '; Status: ' + str(self.status))
