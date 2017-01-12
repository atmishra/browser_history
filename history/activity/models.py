from __future__ import unicode_literals

from django.db import models

from users.models import User
# Create your models here.


class Link(models.Model):
    url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)


class UserHistory(models.Model):
    user = models.ForeignKey(User)
    stack = models.TextField()
    last_ten = models.TextField()
