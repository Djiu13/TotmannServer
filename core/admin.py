from django.contrib import admin
from models import Check, CheckEvent, NotificationReceiver

admin.site.register(Check)
admin.site.register(CheckEvent)
admin.site.register(NotificationReceiver)

