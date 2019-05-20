from django.contrib import admin
from . import models  # includes the models file

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.Response)
admin.site.register(models.UserResponse)
admin.site.register(models.AnonComment)
admin.site.register(models.UserComment)
admin.site.register(models.ChatInstance)
admin.site.register(models.ChatPost)