from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Subject)
admin.site.register(models.Question)
admin.site.register(models.Response)
admin.site.register(models.SiteUsers)