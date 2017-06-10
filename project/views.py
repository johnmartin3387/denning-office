import datetime
import json
from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from functools import wraps
from project.models import *


def property(request):
    return render_to_response('property.html', locals(), context_instance=RequestContext(request))

def matterCode(request):
    return render_to_response('matter_code.html', locals(), context_instance=RequestContext(request))

def contact(request):
    return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

def kjl(request):
    return render_to_response('kjl.html', locals(), context_instance=RequestContext(request))

