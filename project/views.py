import datetime
import json
from collections import OrderedDict

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from functools import wraps
from project.models import *

from django.http import HttpResponse
from geopy.geocoders import Nominatim
import urllib2
import pycountry
import md5

import random

def property_update(request):
    projects = Project.objects.all()
    property = Property()
    mukims = Mukim.objects.all()
    attrs = Attribute.objects.all()

    if len(Contact_Template.objects.filter(type="template_property_denning")) == 0:
        template = Contact_Template()
        template.type = "template_property_denning"
        template.save()

    template = Contact_Template.objects.get(type='template_property_denning')
    if request.POST:
        title_issued = ['title_type_id', 'title_no', 'lot_type_id', 'lot_no', 
            'area', 'area_unit', 'tenure_id', 'lease_expiry_date', 'category_land_use_id',
            'express_condition_id']
        common = ['type', 'individual', 'mukim', 'mukim_val_id', 'daerah', 'negeri', 'title_registeration_date',
            'postal_address', 'assessment_rate', 'annual_quit_rent', 'previous_title', 
            'interest', 'building_type_id', 'building_age', 'pacel_spa_no', 
            'pacel_spa_value', 'building_description_id', 'spa_area', 'spa_area_unit',
            'project_id', 'master_title']
        strata = ['story_no_spa', 'block_no', 'apt_name',
            'access_parcel_no_spa']
        title_issued_strata = ['parcel_no', 'storey_no', 'building_no', 'access_parcel_no', 
            'access_storey_no', 'access_building_no', 'unit_of_share',
            'total_share', 'floor_area']

        interest_data = ['buml_lot', 'malay', 'restriction_against_id', 
            'approving_authority_id', 'other_restriction_id']

        type = request.POST['type']
        individual = True if 'individual' in request.POST else False
        interest = True if 'interest' in request.POST else False

        data = common
        if type == "strata":
            data += strata
        else:
            data += title_issued

        if individual == True:
            data += title_issued_strata
        if interest == True:
            data += interest_data

        data = getDict(request.POST, data)

        property = Property(**data)
        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            property.id = request.POST["id"]

        property.title_registeration_date = None if request.POST['title_registeration_date'] == "" else request.POST['title_registeration_date']
        
        if individual == True:
            property.lease_expiry_date = None if request.POST['lease_expiry_date'] == "" else request.POST['lease_expiry_date']

        property.additional_info = request.POST["custom_data"]
        property.save()
        return redirect('/property/list')
    elif request.GET:
        property = Property.objects.get(pk=request.GET["id"])

    return render_to_response('property/edit.html', locals(), context_instance=RequestContext(request))
def property_list(request):
    properties = Property.objects.all()

    return render_to_response('property/list.html', locals(), context_instance=RequestContext(request))

def property_remove(request):
    try:
        Property.objects.get(pk=request.GET["id"]).delete()
    except:
        pass

    properties = Property.objects.all()
    return render_to_response('property/_list.html', locals(), context_instance=RequestContext(request))

def matterCode_update(request):
    matter_codes = Matter_Code.objects.all()
    attrs = Attribute.objects.all()
    matter_code = Matter_Code()

    if request.POST:
        data = getDict(request.POST, ["code", "matter_tp", "turnaround", "additional_info"])

        matter_code = Matter_Code(**data)

        # if update mode.
        if request.POST["matter_code_id"] != 'None' and \
                request.POST["matter_code_id"] != "":
            matter_code_existed = Matter_Code.objects.get(pk=request.POST["matter_code_id"])
            matter_code.id = matter_code_existed.id

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
    try:
        Matter_Code.objects.get(pk=request.GET["id"]).delete()
    except:
        pass

    matter_codes = Matter_Code.objects.all()
    return render_to_response('matter_code/_list.html', locals(), context_instance=RequestContext(request))


def contact_update(request):
    templates = Contact_Template.objects.all().exclude(type="template_property_denning")
    attrs = Attribute.objects.all()
    countries = list(pycountry.countries)
    location = getLocation()
    contacts = Contact.objects.all().exclude(type="staff")

    zip_code, city, state, country = location["postal"], \
        location["city"], location['region'], location['country']

    if request.POST:
        contact_existed, normal_exited = None, None

        if request.POST["contact_id"] != 'None' and \
                request.POST["contact_id"] != "":
            contact_existed = Contact.objects.get(pk=request.POST["contact_id"])
            normal_exited = Normal.objects.get(contact=contact_existed)
            Phone.objects.filter(contact=contact_existed).delete()
            # contact.delete()
            contact_info_id = contact_existed.info.id
            Contact_Info.objects.filter(pk=contact_info_id).delete()


        # create or update contact information
        address = getDict(request.POST, ["address1", "address2", "address3", "postcode", 
            "town", "state", "country", "fax", "website", "contact_person", "mail_preference"])
        contact_info = Contact_Info(**address)
        contact_info.save()

        # create or update contact
        data = getDict(request.POST, ["id_value", "name",
            "citizenship", "gst_reg_no"])
        contact = Contact(**data)
        if contact_existed != None:
            contact.id = contact_existed.id
        contact.info = contact_info
        contact.id_type_id = request.POST["id_type"]
        contact.title_id = request.POST["title"]
        contact.type = request.POST["template"]
        contact.save()

        # create or update normal contact
        data = getDict(request.POST, ["old_ic", "registered_office", "secretary_id"]) # "secretary",
        normal = Normal(**data)
        if normal_exited != None:
            normal.id = normal_exited.id
        directors = list(set(request.POST.getlist("director[]")))
        normal.directors = ",".join([tp.strip() for tp in directors if tp.strip() != ""])
        normal.contact = contact
        normal.template_id = request.POST["template"]
        normal.additional_info = request.POST["custom_data"]
        normal.save()

        for type in ["phone_home", "phone_office", "phone_mobile"]:
            phone = Phone()
            if request.POST[type] != "":
                phone.phone = request.POST[type]
                phone.type = type
                phone.contact = contact
                phone.save()

        return redirect("/contact/list")
    elif request.GET:
        id = request.GET["id"]
        contact = Contact.objects.get(pk=id)
        normal = Normal.objects.get(contact=contact)
        '''phone_home, phone_office, phone_mobile = 
                validate(Phone.objects.filter(type="home")), 
                validate(Phone.objects.filter(type="office")), 
                validate(Phone.objects.filter(type="mobile"))'''
        zip_code, city, state, country = contact.info.postcode, contact.info.town, \
            contact.info.state, contact.info.country

        phones_tp = Phone.objects.filter(contact=contact)
        phones = {phone.type: phone.phone for phone in phones_tp}

        directors = None
        if normal.directors != "":
            directors = [Contact.objects.get(pk=director) for director in normal.directors.split(",")]

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


def matter_update(request):
    matter = Matter()
    contacts = Staff.objects.all()
    attrs = Attribute.objects.all()
    normals = Normal.objects.all()
    matter_codes = Matter_Code.objects.all()

    if matter.file_number == None:
        matter.file_number = getRandomDigits(8)

    if matter.open_date == None or matter.open_date == "":
        matter.open_date = datetime.datetime.now()

    if "id" in request.GET and request.GET["id"] != "":
        matter = Matter.objects.get(pk=request.GET["id"])

    if request.POST:
        data = getDict(request.POST, ["file_number", "primary_client_id", 
            "file_number2", "partner_in_charge_id", "turnaround", "la_in_charge_id",
            "status_id", "clerk_in_charge_id", "related_id", "matter_code_id",
            "pocket_location", "physical_location", "box_location", "additional_info"])

        matter = Matter(**data)
        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            matter.id = request.POST["id"]

        matter.open_date = None if request.POST['open_date'] == "" else request.POST['open_date']
        matter.close_date = None if request.POST['close_date'] == "" else request.POST['close_date']
        matter.turnaround = 0 if request.POST['turnaround'] == "" else request.POST['turnaround']
        
        matter.save()
        return redirect("/matter/list")

    matters = Matter.objects.all().exclude(file_number=matter.file_number)
    return render_to_response('matter/edit.html', locals(), context_instance=RequestContext(request))
def matter_list(request):
    matters = Matter.objects.all().order_by("-open_date")
    return render_to_response('matter/list.html', locals(), context_instance=RequestContext(request))
def matter_remove(request):
    try:
        Matter.objects.get(pk=request.GET["id"]).delete()
    except:
        pass

    matters = Project.objects.all()
    return render_to_response('matter/_list.html', locals(), context_instance=RequestContext(request))


def staff_update(request):
    contact = Contact()
    staff = Staff()
    attrs = Attribute.objects.all()
    countries = list(pycountry.countries)
    location = getLocation()

    zip_code, city, state, country = location["postal"], \
        location["city"], location['region'], location['country']

    if "id" in request.GET and request.GET["id"] != "":
        contact = Contact.objects.get(pk=request.GET['id'])
        staff = Staff.objects.get(contact=contact)
        phones_tp = Phone.objects.filter(contact=contact)
        phones = {phone.type: phone.phone for phone in phones_tp}

        zip_code, city, state, country = contact.info.postcode, contact.info.town, \
            contact.info.state, contact.info.country

    if request.POST:
        contact_existed, staff_exited = None, None
        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            contact_existed = Contact.objects.get(pk=request.POST["id"])
            staff_exited = Staff.objects.get(contact=contact_existed)
            Phone.objects.filter(contact=contact_existed).delete()
            # contact.delete()
            contact_info_id = contact_existed.info.id
            Contact_Info.objects.filter(pk=contact_info_id).delete()

        # create or update contact information
        address = getDict(request.POST, ["address1", "address2", "address3", "postcode", 
            "town", "state", "country", "fax", "website", "contact_person", "mail_preference"])
        contact_info = Contact_Info(**address)
        contact_info.save()

        # create or update contact
        data = getDict(request.POST, ["id_value", "name", 
            "citizenship"])
        contact = Contact(**data)
        if contact_existed != None:
            contact.id = contact_existed.id
        contact.info = contact_info
        contact.id_type_id = request.POST["id_type"]
        contact.title_id = request.POST["title"]
        contact.type = "staff"
        contact.save()

        # create or update staff
        data = getDict(request.POST, ["login_id", "nickname", 
            "marital", "spouse_name", "number_children", "monthly_salary",
            "prev_adjustment_date", "annual_leave", "date_commenced", "date_ceased",
            "status", "tax_file_no", "socso_no", "epf_no", ""])
        staff = Staff(**data)
        if staff_exited != None:
            staff.id = staff_exited.id
        else:
            staff.password = md5.new(request.POST['password']).hexdigest()

        staff.contact = contact
        staff.qualification_id = request.POST['qualification']
        staff.department_id = request.POST['department']
        staff.position_type_id = request.POST['position_type']
        staff.tenure_employed_id = request.POST['tenure_employed'] if "tenure_employed" in request.POST else None
        staff.date_commenced = None if request.POST['date_commenced'] == "" else request.POST['date_commenced']
        staff.date_ceased = None if request.POST['date_ceased'] == "" else request.POST['date_ceased']
        staff.prev_adjustment_date = None if request.POST['prev_adjustment_date'] == "" else request.POST['prev_adjustment_date']
        # staff.privilege_id = request.POST[""]
        staff.save()

        for type in ["phone_home", "phone_office", "phone_mobile"]:
            phone = Phone()
            if request.POST[type] != "":
                phone.phone = request.POST[type]
                phone.type = type
                phone.contact = contact
                phone.save()

        return redirect("/staff/list")

    return render_to_response('staff/edit.html', locals(), context_instance=RequestContext(request))
def staff_list(request):
    staffs = Contact.objects.filter(type="staff")
    details = []
    for staff in staffs:
        details.append(Staff.objects.get(contact=staff))

    return render_to_response('staff/list.html', locals(), context_instance=RequestContext(request))

def staff_remove(request):
    contact = Contact.objects.get(pk=request.GET["id"])
    Staff.objects.filter(contact=contact).delete()
    Phone.objects.filter(contact=contact).delete()
    contact.delete()
    contact_info_id = contact.info.id
    Contact_Info.objects.filter(pk=contact_info_id).delete()

    staffs = Contact.objects.filter(type="staff")
    details = []
    for staff in staffs:
        details.append(Staff.objects.get(contact=staff))

    return render_to_response('staff/_list.html', locals(), context_instance=RequestContext(request))

def states(request):
    res = ""
    if "country_code" in request.GET:
        country_code = request.GET["country_code"]
        location = getLocation()
        default_state = location['region'] if request.GET['state'] == "" else request.GET['state']

        states = list(pycountry.subdivisions.get(country_code=country_code))
        
        states = [state.name for state in states]
        states.sort()

        for state in states:
            selected = ""
            state = state.replace("Wilayah Persekutuan", "").strip()
            if default_state in state:
                selected = "selected"
            res += "<option value=\"%s\" %s>%s</option>" % (state, selected, state)

    return HttpResponse(res)

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

def getLocation():
    location = urllib2.urlopen("http://ipinfo.io/?callback=jQuery112407295098996076215_1498225508165&_=1498225508166").read()
    try:
        location = json.loads("{%s}" % location.strip().split("({")[1].split("});")[0])
        return location
    except:
        return dict()

def getIP():
    geolocator = Nominatim()
    location = geolocator.geocode("Jalan Desa Utama")
    print(location.raw)

def project_update(request):
    project = Project()
    attrs = Attribute.objects.all()
    contacts = Normal.objects.all()

    if "id" in request.GET:
        project = Project.objects.get(pk=request.GET['id'])
    if request.POST:
        data = getDict(request.POST, ["name", "phase", "license_date", "approval",
            "location", "license_no", "note1", "note2", "local_authority_id",
            "permit_no", "developer_id",  "proprietor_id", "land_tenure_id",
            "hda_no", "encumbrances_id", "bank_id"])
        project = Project(**data)

        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            project.id = request.POST["id"]

        project.permit_commencement_date = None if request.POST['permit_commencement_date'] == "" else request.POST['permit_commencement_date']
        project.permit_expiry_date = None if request.POST['permit_expiry_date'] == "" else request.POST['permit_expiry_date']
        project.complete_date = None if request.POST['complete_date'] == "" else request.POST['complete_date']
        project.lease_expiry_date = None if request.POST['lease_expiry_date'] == "" else request.POST['lease_expiry_date']
        project.save()

        return redirect("/project/list")

    return render_to_response('project/edit.html', locals(), context_instance=RequestContext(request))

def project_list(request):
    projects = Project.objects.all()

    return render_to_response('project/list.html', locals(), context_instance=RequestContext(request))
def project_remove(request):
    Project.objects.get(pk=request.GET["id"]).delete()
    projects = Project.objects.all()
    return render_to_response('project/_list.html', locals(), context_instance=RequestContext(request))

def property_template(request):
    template = Contact_Template.objects.get(type="template_property_denning")
    template.json = request.GET["json"]
    template.save()

    return HttpResponse(str(template.id))

def mukim_update(request):
    mukim = Mukim()
    if "id" in request.GET:
        mukim = Mukim.objects.get(pk=request.GET["id"])

    if request.POST:
        data = getDict(request.POST, ["mukim", "district", "state", "code"])
        mukim = Mukim(**data)
        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            mukim.id = request.POST["id"]
        mukim.save()

        return redirect("/mukim/list")

    return render_to_response('mukim/edit.html', locals(), context_instance=RequestContext(request))
def mukim_list(request):
    mukims = Mukim.objects.all()
    return render_to_response('mukim/list.html', locals(), context_instance=RequestContext(request))
def mukim_remove(request):
    Mukim.objects.get(pk=request.GET['id']).delete()
    return render_to_response('mukim/_list.html', locals(), context_instance=RequestContext(request))

def getRandomDigits(length):
    return ''.join(["%s" % random.randint(0, 9) for num in range(0, length)])
