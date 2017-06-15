import datetime
import json
from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from functools import wraps
from project.models import *


def property_update(request):
    return render_to_response('property/edit.html', locals(), context_instance=RequestContext(request))
def property_list(request):
    properties = Property.objects.filter(deleted=False)

    return render_to_response('property/list.html', locals(), context_instance=RequestContext(request))

def matterCode_update(request):
    return render_to_response('matter_code/edit.html', locals(), context_instance=RequestContext(request))
def matterCode_list(request):
    return render_to_response('matter_code/edit.html', locals(), context_instance=RequestContext(request))

def contact_update(request):
    templates = Contact_Template.objects.all()
    if request.POST:
        contact = Contact()
        address = getDict(request.POST, ["address1", "address2", "address3", "postcode", 
            "town", "state", "country", "fax", "website", "contact_person", "mail_preference"])
        contact_info = Contact_Info(**address)
        contact_info.save()
        print request.POST.getlist("director[]")
        data = getDict(request.POST, ["id_type", "id_value", "name", "title", 
            "citizenship"])
        contact = Contact(**data)
        contact.info = contact_info
        contact.type = request.POST["template"]
        contact.save()

        '''data = getDict(request.POST, ["old_ic", "registered_office", "secretary", "template"])
        normal_contact = Normal(**data)
        normal_contact = ",".join(request.POST.getlist("director[]"))
        normal_contact.save()'''

    return render_to_response('contact/edit.html', locals(), context_instance=RequestContext(request))
def contact_list(request):
    contacts = Contact.objects.all().exclude(type="staff")

    return render_to_response('contact/list.html', locals(), context_instance=RequestContext(request))

def getDict(seed, keys):
    temp = dict()
    for key in keys:
        temp[key] = seed[key]
    return temp