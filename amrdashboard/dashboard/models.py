from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,on_delete=models.CASCADE,)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class PathTest(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    testid = models.CharField(max_length=25)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.test