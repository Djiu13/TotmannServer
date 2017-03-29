from django.contrib import admin
from core.models import Check, CheckEvent, NotificationReceiver

admin.site.register(Check)
admin.site.register(CheckEvent)
admin.site.register(NotificationReceiver)

