from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Link(models.Model):
    url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
