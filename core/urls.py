from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^([^/]+)/start', views.event_start, name='event-start'),
                       url(r'^([^/]+)/finished', views.event_finished, name='event-finished'),
                       url(r'^([^/]+)/log', views.event_log, name='event-log'),
)
