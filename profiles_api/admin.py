from django.contrib import admin

from profiles_api import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)

""" created superuser details
 email: a@gmail.com
 name: aayush
 pass: ad123456 """