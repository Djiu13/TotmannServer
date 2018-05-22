from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^list$', views.list, name='list'),
    url(r'^list/(?P<tag_selected>.+)', views.list, name='list_filter_by_tag'),
    url(r'^timeline$', views.timeline, name='timeline'),
    url(r'^details/(?P<apikey>[a-zA-Z0-9-_]+)', views.details, name='details'),
    url(r'^toggle', views.toggle, name='toggle'),
    url(r'^add', views.check_add, name='check-add'),
    url(r'^notification-add', views.notification_add, name='notification-add'),
    url(r'^confirm/(?P<token>[a-fA-F0-9]+)', views.confirm_email, name='confirm-email'),
    url(r'^notification-remove', views.notification_remove, name='notification-remove'),
    #                       url(r'^([a-zA-Z0-9-_]+)/finished', views.event_finished, name='rest-event-finished'),
    #                       url(r'^([a-zA-Z0-9-_]+)/log', views.event_log, name='rest-event-log'),
]
