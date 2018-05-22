from django.shortcuts import render
from . import models
from django.views.decorators.http import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

@csrf_exempt
@require_http_methods(["POST"])
def event_start(request, uuid):
    check = get_object_or_404(models.Check, apikey=uuid)
    event = models.CheckEvent(source=check, event=models.CheckEvent.EVENT_START)
    event.save()
    return HttpResponse("OK", content_type="text/plain")

@csrf_exempt
@require_http_methods(["POST"])
def event_log(request, uuid):
    body = request.body.decode('utf-8', errors='replace')
    check = get_object_or_404(models.Check, apikey=uuid)
    event = models.CheckEvent(source=check,
                              event=models.CheckEvent.EVENT_LOG,
                              content=body)
    event.save()
    return HttpResponse("OK", content_type="text/plain")

@csrf_exempt
@require_http_methods(["POST"])
def event_finished(request, uuid):
    check = get_object_or_404(models.Check, apikey=uuid)
    c = request.body.decode('utf-8', errors='replace')
    if len(c) == 0:
        c = "0"
    event = models.CheckEvent(source=check,
                              event=models.CheckEvent.EVENT_FINISHED,
                              content=c)
    event.save()
    return HttpResponse("OK", content_type="text/plain")

