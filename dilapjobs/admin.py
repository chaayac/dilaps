from django.contrib import admin

from .models import job, logs

admin.site.register(job)
admin.site.register(logs)
# Register your models here.
