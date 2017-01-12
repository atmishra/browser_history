from django.contrib import admin
from .models import Link, UserHistory


class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'url']


class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'stack', 'last_ten']

admin.site.register(Link, LinkAdmin)
admin.site.register(UserHistory, UserHistoryAdmin)
# Register your models here.
