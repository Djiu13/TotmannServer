from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^([^/]+)/start', views.event_start, name='event-start'),
	url(r'^([^/]+)/finished', views.event_finished, name='event-finished'),
	url(r'^([^/]+)/log', views.event_log, name='event-log')
]
