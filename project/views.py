import datetime
import json
from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from functools import wraps
from project.models import *

from django.http import HttpResponse

def property_update(request):
    

    return render_to_response('property/edit.html', locals(), context_instance=RequestContext(request))
def property_list(request):
    properties = Property.objects.filter(deleted=False)

    return render_to_response('property/list.html', locals(), context_instance=RequestContext(request))

def matterCode_update(request):
    matter_codes = Matter_Code.objects.all()
    attrs = Attribute.objects.all()
    matter_code = Matter_Code()

    if request.POST:
        data = getDict(request.POST, ["code", "matter_tp", "turnaround", "additional_info"])

        if request.POST["matter_code_id"] != 'None' and \
                request.POST["matter_code_id"] != "":
            Matter_Code.objects.get(pk=request.POST["matter_code_id"]).delete()

        matter_code = Matter_Code(**data)
        matter_code.category_id = request.POST["category"]
        matter_code.department_id = request.POST["department"]
        # matter_code.related_id = request.POST["related"]
        matter_code.save()
        return redirect("/matter-code/list")
    elif request.GET:
    	matter_code = Matter_Code.objects.get(pk=request.GET["id"])

    return render_to_response('matter_code/edit.html', locals(), context_instance=RequestContext(request))
def matterCode_list(request):
    matter_codes = Matter_Code.objects.all()
    return render_to_response('matter_code/list.html', locals(), context_instance=RequestContext(request))
def matterCode_remove(request):
    Matter_Code.objects.get(pk=request.GET["id"]).delete()
    matter_codes = Matter_Code.objects.all()
    return render_to_response('matter_code/_list.html', locals(), context_instance=RequestContext(request))


def contact_update(request):
    templates = Contact_Template.objects.all()
    attrs = Attribute.objects.all()

    if request.POST:
        if request.POST["contact_id"] != 'None' and \
                request.POST["contact_id"] != "":
            contact = Contact.objects.get(pk=request.POST["contact_id"])
            Normal.objects.filter(contact=contact).delete()
            Phone.objects.filter(contact=contact).delete()
            contact.delete()
            contact_info_id = contact.info.id
            Contact_Info.objects.filter(pk=contact_info_id).delete()

        address = getDict(request.POST, ["address1", "address2", "address3", "postcode", 
            "town", "state", "country", "fax", "website", "contact_person", "mail_preference"])
        contact_info = Contact_Info(**address)
        contact_info.save()

        data = getDict(request.POST, ["id_value", "name", "title", 
            "citizenship", "gst_reg_no"])
        contact = Contact(**data)
        contact.info = contact_info
        contact.id_type_id = request.POST["id_type"]
        contact.type = request.POST["template"]
        contact.save()

        data = getDict(request.POST, ["old_ic", "registered_office"]) # "secretary",
        normal_contact = Normal(**data)
        normal_contact.directors = ",".join(request.POST.getlist("director[]"))
        normal_contact.contact = contact
        normal_contact.template_id = request.POST["template"]
        normal_contact.save()

        '''data = getDict(request.POST, ["phone_home", "phone_office", "phone_mobile"])
        for key in data:
            if data[key] == "":
                continue
            type = key.split("-")[0]
            phone = Phone()
            phone.phone = data[key]
            phone.type = type
            phone.contact = contact
            phone.save()'''
        return redirect("/contact/list")
    elif request.GET:
        id = request.GET["id"]
        contact = Contact.objects.get(pk=id)
        normal = Normal.objects.get(contact=contact)
        '''phone_home, phone_office, phone_mobile = 
                validate(Phone.objects.filter(type="home")), 
                validate(Phone.objects.filter(type="office")), 
                validate(Phone.objects.filter(type="mobile"))'''

    return render_to_response('contact/edit.html', locals(), context_instance=RequestContext(request))

def contact_list(request):
    contacts = Contact.objects.all().exclude(type="staff")
    return render_to_response('contact/list.html', locals(), context_instance=RequestContext(request))

def contact_remove(request):
    contact = Contact.objects.get(pk=request.GET["id"])
    Normal.objects.filter(contact=contact).delete()
    Phone.objects.filter(contact=contact).delete()
    contact.delete()
    contact_info_id = contact.info.id
    Contact_Info.objects.filter(pk=contact_info_id).delete()

    contacts = Contact.objects.all().exclude(type="staff")
    return render_to_response('contact/_list.html', locals(), context_instance=RequestContext(request))

def getDict(seed, keys):
    temp = dict()
    for key in keys:
        try:
            temp[key] = seed[key]
        except:
            pass
    return temp

def validate(value):
	try:
		return value[0]
	except:
		return ""