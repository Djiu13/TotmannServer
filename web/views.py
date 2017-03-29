from django.views.decorators.http import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from core import models
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import re
from django.contrib.auth.decorators import login_required
from forms import EditCheckForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tagging.models import Tag, TaggedItem

def home(request):
    return render(request, 'web/home.html', {} )

@login_required
def list(request, tag_selected=None):
    if not tag_selected:
        startSet = models.Check.objects
    else:
        startSet = TaggedItem.objects.get_by_model(models.Check, Tag.objects.get(name=tag_selected))
    checks_enabled = startSet.filter(enabled=True, owner=request.user).order_by('prefix', 'name').all()
    checks_disabled = startSet.filter(enabled=False, owner=request.user).order_by('prefix', 'name').all()
    notifications = models.NotificationReceiver.objects.filter(owner=request.user).all()
    tags = models.Check.tags.usage(filters={'owner': request.user, 'enabled': True})
        
        
    return render(request, 'web/list.html', {
        'checks_enabled' : checks_enabled,
        'checks_disabled' : checks_disabled,
        'notifications' : notifications,
        'tags': tags,
        'tag_selected': tag_selected,
        })

@login_required
def details(request, apikey):
    check = get_object_or_404(models.Check, apikey=apikey, owner=request.user)
    events = models.CheckEvent.objects.filter(source=check).order_by('-timestamp').all()
    if request.method == 'POST' and request.POST['action'] == 'remove':
        for e in events.all():
            e.delete()
        check.delete()
        return HttpResponseRedirect(reverse('web:list'))

    if request.method == "POST":
        form = EditCheckForm(request.user, request.POST, instance=check)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web:details', kwargs={'apikey': apikey}))
    else:
        form = EditCheckForm(request.user, instance=check)

    paginator = Paginator(events, 20, orphans=5)
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
        
    return render(request, 'web/details.html', {
        'check': check,
        'events': events,
        'form': form,
        })


@login_required
@require_http_methods(["POST"])
def toggle(request):
    check = get_object_or_404(models.Check, apikey=request.POST['apikey'], owner=request.user)
    check.enabled = not check.enabled
    check.save()
    return HttpResponseRedirect(reverse('web:list'))

@login_required
@require_http_methods(["POST"])
def check_add(request):
    if len(request.POST['name']) == 0:
        return HttpResponseRedirect(reverse('web:list'))        
    check = models.Check(owner=request.user, name=request.POST['name'])
    check.save()
    check.notifications = models.NotificationReceiver.objects.filter(owner=request.user).all()
    check.save()
    return HttpResponseRedirect(reverse('web:details', kwargs={'apikey': check.apikey}))

@login_required
@require_http_methods(["POST"])
def notification_remove(request):
    r = get_object_or_404(models.NotificationReceiver, id=request.POST['remove-notification'], owner=request.user)
    r.delete()
    return HttpResponseRedirect(reverse('web:list'))

@login_required
@require_http_methods(["POST"])
def notification_add(request):
    email = request.POST['email']
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        r = models.NotificationReceiver(address = email, owner = request.user)
        r.send_confirmation_token(request)
        r.save()
    return HttpResponseRedirect(reverse('web:list'))

@login_required
def confirm_email(request, token):
    n = get_object_or_404(models.NotificationReceiver, owner=request.user, confirmation_token=token)
    n.confirmation_token = None
    n.save()
    return HttpResponseRedirect(reverse('web:list'))
