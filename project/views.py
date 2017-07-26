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

from denning_office import settings
from django.http import JsonResponse, HttpResponseForbidden
from project.utils import *

# Login Required decorator
def login_required():
    def login_decorator(function):
        @wraps(function)
        def wrapped_function(request):

            # if a user is not authorized, redirect to login page
            if 'user' not in request.session or request.session['user'] is None:
                return redirect("/login")
            # otherwise, go on the request
            else:
                staff = Staff.objects.get(group_id=request.session["user"]["group_id"], \
                            company_id=request.session["user"]["company_id"])
                if "verification" not in request.build_absolute_uri() and staff.email_verification != "-1":
                    return render_to_response('verification.html', locals(), context_instance=RequestContext(request))
                return function(request)

        return wrapped_function

    return login_decorator

def login(request):
    error = 'none'
    request.session['user'] = None

    if 'username' in request.POST:

        # get username and password from request.
        username = request.POST['username']
        password = request.POST['password']

        print username, password
        login_staff = Staff.objects.filter(login_id=username, password=md5.new(request.POST['password']).hexdigest())

        # check whether the user is in database or not
        if len(login_staff):
            try:
                request.session['user'] = {
                    # "id": user[0].id,
                    "id": login_staff[0].id,
                    "username": username, #user[0].email,
                    "group": login_staff[0].group.name,
                    "group_id": login_staff[0].group.id,
                    "company": login_staff[0].company.name,
                    "company_id": login_staff[0].company.id,
                    "email_verification": True
                }
            except:
                request.session['user'] = {
                    "id": login_staff[0].id,
                    # "id": user[0].id,
                    "username": username, #user[0].email,
                    "group": login_staff[0].group.name,
                    "group_id": login_staff[0].group.id,
                    "company": None,
                    "company_id": None,
                    "email_verification": True
                }                

            if login_staff[0].email_verification != "-1":
                request.session['user']["email_verification"] = False
                return render_to_response('verification.html', locals(), context_instance=RequestContext(request))

            return redirect("/matter/list")

        else:
            error = 'block'

    return render_to_response('login.html', {'error':error}, context_instance=RequestContext(request))

def getAuthorization(request, target=None):
    group = Group.objects.get(pk=request.session["user"]['group_id'])
    try:
        privileges = group.privilege_json.split(",")
    except:
        privileges = []

    res = dict()
    if target == None:
        for privilege in settings.PRIVILEGE_SETTING:
            res[privilege] = dict()
            for role in ["create", "update", "remove", "view"]:
                if "%s_%s" % (privilege, role) in privileges:
                    res[privilege][role] = True
                else:
                    res[privilege][role] = False
    else:
        res = dict()
        for role in ["create", "update", "remove", "view"]:
            if "%s_%s" % (target, role) in privileges:
                res[role] = True
            else:
                res[role] = False
    return res

def getFullAuthorization():
    res = []
    for privilege in settings.PRIVILEGE_SETTING:
        res.append(privilege)
        for role in ['create', 'update', 'remove', "view"]:
            res.append("%s_%s" % (privilege, role))
    return ",".join(res)

def logout(request):
    request.session['user'] = None
    return redirect("/login")

def privilege_settings(request):
    if 'user' not in request.session or request.session['user'] == None or \
               request.session['user']['group'] != 'Administrator':
        return redirect("/login")

    groups = Group.objects.filter(company_id=request.session['user']['company_id'])
    return render_to_response('privilege/settings.html', locals(), context_instance=RequestContext(request))

@login_required()
def start_page(request):
    return redirect("/matter/list")

@login_required()
def property_update(request):
    auth = getAuthorization(request, "property")

    projects = Project.objects.all()
    property = Property()
    mukims = Mukim.objects.all()
    attrs = Attribute.objects.all()

    if len(Contact_Template.objects.filter(type="template_property_denning")) == 0:
        template = Contact_Template()
        template.type = "template_property_denning"
        template.json = "[]"
        template.save()

    template = Contact_Template.objects.get(type='template_property_denning')
    if request.POST:
        if auth["update"] == False:
            return HttpResponseForbidden()
            
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
        if auth["update"] == False:
            return HttpResponseForbidden()
            
        property = Property.objects.get(pk=request.GET["id"])

    return render_to_response('property/edit.html', locals(), context_instance=RequestContext(request))

@login_required()
def property_list(request):
    auth = getAuthorization(request, "property")
    properties = Property.objects.all()

    return render_to_response('property/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def property_remove(request):
    auth = getAuthorization(request, "property")
    if auth["remove"] == False:
        return HttpResponseForbidden()

    try:
        Property.objects.get(pk=request.GET["id"]).delete()
    except:
        pass

    properties = Property.objects.all()
    return render_to_response('property/_list.html', locals(), context_instance=RequestContext(request))

@login_required()
def matterCode_update(request):
    auth = getAuthorization(request, "mattercode")

    matter_codes = Matter_Code.objects.all()
    attrs = Attribute.objects.all()
    matter_code = Matter_Code()

    if request.POST:
        if auth["update"] == False:
            return HttpResponseForbidden()

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
        if auth["update"] == False:
            return HttpResponseForbidden()

        matter_code = Matter_Code.objects.get(pk=request.GET["id"])

    return render_to_response('matter_code/edit.html', locals(), context_instance=RequestContext(request))

@login_required()
def matterCode_list(request):
    auth = getAuthorization(request, "mattercode")

    matter_codes = Matter_Code.objects.all()
    return render_to_response('matter_code/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def matterCode_remove(request):
    auth = getAuthorization(request, "mattercode")
    if auth["remove"] == False:
        return HttpResponseForbidden()

    try:
        Matter_Code.objects.get(pk=request.GET["id"]).delete()
    except:
        pass

    matter_codes = Matter_Code.objects.all()
    return render_to_response('matter_code/_list.html', locals(), context_instance=RequestContext(request))

@login_required()
def contact_update(request):
    auth = getAuthorization(request, "contact")
    templates = Contact_Template.objects.all().exclude(type="template_property_denning")
    attrs = Attribute.objects.all()
    countries = list(pycountry.countries)
    location = getLocation()
    contacts = Contact.objects.all().exclude(type="staff")

    try:
        zip_code, city, state, country = location["postal"] if "postal" in location else "", \
            location["city"], location['region'], location['country']
    except:
        zip_code, city, state, country = "", "", "", ""

    if request.POST:
        if auth["update"] == False:
            return HttpResponseForbidden()

        contact_existed, normal_exited = None, None

        if request.POST["contact_id"] != 'None' and \
                request.POST["contact_id"] != "":
            contact_existed = Contact.objects.get(pk=request.POST["contact_id"])
            normal_exited = Normal.objects.get(contact=contact_existed)
            Phone.objects.filter(contact=contact_existed).exclude(type="personal").delete()
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
        if auth["update"] == False:
            return HttpResponseForbidden()
            
        id = request.GET["id"]
        contact = Contact.objects.get(pk=id)
        normal = Normal.objects.get(contact=contact)
        '''phone_home, phone_office, phone_mobile = 
                validate(Phone.objects.filter(type="home")), 
                validate(Phone.objects.filter(type="office")), 
                validate(Phone.objects.filter(type="mobile"))'''
        zip_code, city, state, country = contact.info.postcode, contact.info.town, \
            contact.info.state, contact.info.country

        phones_tp = Phone.objects.filter(contact=contact).exclude(type="personal")
        phones = {phone.type: phone.phone for phone in phones_tp}

        directors = None
        if normal.directors != "":
            directors = [Contact.objects.get(pk=director) for director in normal.directors.split(",")]

    return render_to_response('contact/edit.html', locals(), context_instance=RequestContext(request))

@login_required()
def contact_list(request):
    auth = getAuthorization(request, "contact")

    contacts = Contact.objects.all().exclude(type="staff")
    return render_to_response('contact/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def contact_remove(request):
    auth = getAuthorization(request, "contact")
    if auth["remove"] == False:
        return HttpResponseForbidden()

    contact = Contact.objects.get(pk=request.GET["id"])
    Normal.objects.filter(contact=contact).delete()
    Phone.objects.filter(contact=contact).exclude(type="personal").delete()
    contact.delete()
    contact_info_id = contact.info.id
    Contact_Info.objects.filter(pk=contact_info_id).delete()

    contacts = Contact.objects.all().exclude(type="staff")
    return render_to_response('contact/_list.html', locals(), context_instance=RequestContext(request))

@login_required()
def matter_update(request):
    auth = getAuthorization(request, "matter")

    matter = Matter()
    contacts = Staff.objects.all().exclude(group__name="Super Administrator")
    attrs = Attribute.objects.all()
    normals = Normal.objects.all()
    matter_codes = Matter_Code.objects.all()

    if matter.file_number == None:
        matter.file_number = getRandomDigits(8)

    if matter.open_date == None or matter.open_date == "":
        matter.open_date = datetime.datetime.now()

    if "id" in request.GET and request.GET["id"] != "":
        if auth["update"] == False:
            return HttpResponseForbidden()
            
        matter = Matter.objects.get(pk=request.GET["id"])

    if request.POST:
        if auth["update"] == False:
            return HttpResponseForbidden()

        data = getDict(request.POST, ["file_number", "primary_client_id", 
            "file_number2", "partner_in_charge_id", "turnaround", "la_in_charge_id",
            "status_id", "clerk_in_charge_id", "related_id", "matter_code_id",
            "pocket_location", "physical_location", "box_location"])

        matter = Matter(**data)

        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            matter.id = request.POST["id"]

        matter.open_date = None if request.POST['open_date'] == "" else request.POST['open_date']
        matter.close_date = None if request.POST['close_date'] == "" else request.POST['close_date']
        matter.turnaround = 0 if request.POST['turnaround'] == "" else request.POST['turnaround']
        matter.additional_info = request.POST['custom_data']

        matter.save()
        return redirect("/matter/list")

    matters = Matter.objects.all().exclude(file_number=matter.file_number)
    return render_to_response('matter/edit.html', locals(), context_instance=RequestContext(request))

@login_required()
def matter_list(request):
    auth = getAuthorization(request, "matter")
    matters = Matter.objects.all().order_by("-open_date")
    return render_to_response('matter/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def matter_remove(request):
    auth = getAuthorization(request, "matter")
    if auth["remove"] == False:
        return HttpResponseForbidden()

    try:
        Matter.objects.get(pk=request.GET["id"]).delete()
    except:
        pass

    matters = Matter.objects.all()
    return render_to_response('matter/_list.html', locals(), context_instance=RequestContext(request))

@login_required()
def staff_update(request):
    auth = getAuthorization(request, "staff")
    #if request.session['user']['group'] != "Super Administrator":
    #    return HttpResponseForbidden()

    auth = getAuthorization(request, "staff")

    contact = Contact()
    staff = Staff()
    attrs = Attribute.objects.all()
    countries = list(pycountry.countries)
    location = getLocation()

    try:
        zip_code, city, state, country = location["postal"] if "postal" in location else "", \
            location["city"], location['region'], location['country']
    except:
        zip_code, city, state, country = "", "", "", ""
    zip_code, city, state, country = location["postal"], \
        location["city"], location['region'], location['country']
    groups = Group.objects.filter(company_id=request.session["user"]["company_id"]).exclude(name="Administrator")

    if "id" in request.GET and request.GET["id"] != "":
        if auth["update"] == False:
            return HttpResponseForbidden()
            
        contact = Contact.objects.get(pk=request.GET['id'])
        staff = Staff.objects.get(contact=contact)
        phones_tp = Phone.objects.filter(contact=contact).exclude(type="personal")
        phones = {phone.type: phone.phone for phone in phones_tp}

        zip_code, city, state, country = contact.info.postcode, contact.info.town, \
            contact.info.state, contact.info.country

    if request.POST:
        if auth["update"] == False:
            return HttpResponseForbidden()
            
        contact_existed, staff_exited = None, None
        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            contact_existed = Contact.objects.get(pk=request.POST["id"])
            staff_exited = Staff.objects.get(contact=contact_existed)
            Phone.objects.filter(contact=contact_existed).exclude(type="personal").delete()
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
            staff.password = staff_exited.password
            staff.login_id = staff_exited.login_id
        else:
            staff.password = md5.new(request.POST['password']).hexdigest()

        staff.contact = contact
        staff.qualification_id = request.POST['qualification'] if "tenure_employed" in request.POST else None
        staff.department_id = request.POST['department']
        staff.position_type_id = request.POST['position_type']
        staff.tenure_employed_id = request.POST['tenure_employed'] if "tenure_employed" in request.POST else None
        staff.date_commenced = None if request.POST['date_commenced'] == "" else request.POST['date_commenced']
        staff.date_ceased = None if request.POST['date_ceased'] == "" else request.POST['date_ceased']
        staff.prev_adjustment_date = None if request.POST['prev_adjustment_date'] == "" else request.POST['prev_adjustment_date']
        staff.company_id = request.session['user']['company_id']
        staff.group_id = request.POST["group"]
        # staff.privilege_id = request.POST[""]
        staff.save()

        print request.POST['date_commenced']
        print staff.date_commenced 

        for type in ["phone_home", "phone_office", "phone_mobile"]:
            phone = Phone()
            if request.POST[type] != "":
                phone.phone = request.POST[type]
                phone.type = type
                phone.contact = contact
                phone.save()

        return redirect("/staff/list")

    return render_to_response('staff/edit.html', locals(), context_instance=RequestContext(request))

@login_required()
def staff_list(request):
    auth = getAuthorization(request, "staff")
    details = Staff.objects.filter(company_id=request.session["user"]["company_id"]).exclude(group__name="Administrator")
    staffs = []
    for detail in details:
        staffs.append(detail.contact)

    return render_to_response('staff/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def staff_remove(request):
    auth = getAuthorization(request, "staff")
    if auth["remove"] == False:
        return HttpResponseForbidden()
    contact = Contact.objects.get(pk=request.GET["id"])
    Staff.objects.filter(contact=contact).delete()
    Phone.objects.filter(contact=contact).exclude(type="personal").delete()
    contact.delete()
    contact_info_id = contact.info.id
    Contact_Info.objects.filter(pk=contact_info_id).delete()

    details = Staff.objects.filter(company_id=request.session["user"]["company_id"]).exclude(group__name="Administrator")
    staffs = []
    for detail in details:
        staffs.append(detail.contact)

    return render_to_response('staff/_list.html', locals(), context_instance=RequestContext(request))

# @login_required()
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

@login_required()
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

def company_update(request):
    countries = list(pycountry.countries)
    location = getLocation()
    print location
    contacts = Contact.objects.all().exclude(type="staff")

    attrs = Attribute.objects.all()
    period = [idx for idx in range(1, 7)]

    if request.POST:
        # create or update contact information
        address = getDict(request.POST, ["address1", "address2", "address3", "postcode", 
            "town", "state", "country", "website", "mail_preference"])
        contact_info = Contact_Info(**address)
        contact_info.save()

        # create or update company
        data = ["name", "initials", "description1_id", "description2_id", 
            "fax", "fax2", "commencement_date", "partner_label", "partner_qualification",
            "la_label", "tax_invoice", "quotation", "receipt", "message"]

        gst_registered = ["gst_rate", "registration_no", "register_date", "effective_date",  "taxable_period"]

        if "gst_registered" in request.POST:
            data = data + gst_registered

        data = getDict(request.POST, data)

        company = Company(**data)
        if request.POST["id"] != 'None' and \
                request.POST["id"] != "":
            company_existed = Company.objects.get(pk=request.POST["id"])
            company.id = company_existed.id
            Phone_Company.objects.filter(company_id=request.POST["id"]).delete()
            Contact_Info.objects.filter(pk=company.info_id).delete()

            staff = Staff.objects.get(company_id=request.POST["id"], group__name="Administrator")
            staff.contact.name = request.POST["login_name"]
            staff.contact.save()

            Phone.objects.filter(contact=staff.contact, type="personal").delete()
            phone_personal = Phone()
            phone_personal.phone = request.POST["phone_personal"]
            phone_personal.contact = staff.contact
            phone_personal.type = "personal"
            phone_personal.save()
        else:
            contact = Contact()
            contact.name = request.POST["login_name"]
            contact.save()

            staff = Staff()
            staff.contact = contact
            staff.login_id = request.POST["login_id"]
            staff.password = md5.new(request.POST["password"]).hexdigest()

            phone_personal = Phone()
            phone_personal.phone = request.POST["phone_personal"]
            phone_personal.contact = contact
            phone_personal.type = "personal"
            phone_personal.save()
            
            # set code for email verification
            staff.email_verification = getRandomDigits(15)

        company.info = contact_info
        company.partner = "@@@".join(request.POST.getlist("partner[]"))
        company.la_clerk = "@@@".join(request.POST.getlist("la_clerk[]"))

        if "gst_registered" in request.POST:
            company.gst_registered = True
            company.partner_qualification = "@@@".join(request.POST.getlist("partner_qualifications[]"))
            company.commencement_date = None if request.POST['commencement_date'] == "" else request.POST['commencement_date']
            company.register_date = None if request.POST['register_date'] == "" else request.POST['register_date']
            company.effective_date = None if request.POST['effective_date'] == "" else request.POST['effective_date']
        else:
            company.gst_registered = False

        company.save()

        staff.company = company
        if "group" in request.POST:
            staff.group_id = request.POST["group"]
        else:
            if len(Group.objects.filter(company=company, name="Administrator")):
                group = Group.objects.filter(company=company, name="Administrator")[0]
            else:
                group = Group()
                group.name = "Administrator"
                group.company = company
                group.privilege_json = getFullAuthorization()
                group.save()

            staff.group = group

        staff.save()
        if request.POST["id"] == 'None' or \
                request.POST["id"] == "":

            request.session['user'] = {
                "id": staff.id,
                # "id": user[0].id,
                "username": staff.login_id, #user[0].email,
                "group": staff.group.name,
                "group_id": staff.group.id,
                "company": staff.company.name,
                "company_id": staff.company.id,
                "email_verification": False
            }

            url = "http://%s:%s/verification?code=%s" % (settings.SERVER_IP, request.META["SERVER_PORT"], staff.email_verification)
            body = "Please verify your email: <a href='%s'>%s</a>" % (url, url)

            # send email for meter status
            send_email(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.DEFAULT_FROM_EMAIL, \
                          request.POST['login_id'], "Email verification", body)

            return redirect("/verification")
            

        for type in ["phone_home", "phone_office", "phone_mobile"]:
            phone = Phone_Company()
            if request.POST[type] != "":
                phone.phone = request.POST[type]
                phone.type = type
                phone.company = company
                phone.save()


    if 'user' in request.session and request.session['user'] != None and \
               request.session['user']['group'] == 'Administrator':
        company = Company.objects.get(pk=request.session['user']['company_id'])

        zip_code, city, state, country = company.info.postcode, company.info.town, \
            company.info.state, company.info.country

        phones_tp = Phone_Company.objects.filter(company=company)
        phones = {phone.type: phone.phone for phone in phones_tp}

        staff = Staff.objects.get(company=company, group_id=request.session["user"]["group_id"])
        try:
            phone_personal = Phone.objects.filter(contact=staff.contact, type="personal")[0].phone
        except:
            phone_personal = ""

        partners, clerks, partner_qualifications = company.partner.split("@@@"), company.la_clerk.split("@@@"), \
                            company.partner_qualification.split("@@@")
    else:
        company = Company()

        try:
            zip_code, city, state, country = location["postal"] if "postal" in location else "", \
                location["city"], location['region'], location['country']
        except:
            zip_code, city, state, country = "", "", "", ""

    return render_to_response('company/edit.html', locals(), context_instance=RequestContext(request))

@login_required()
def company_list(request):
    if request.session["user"]["group"] != "Super Administrator":
        return HttpResponseForbidden()

    administrators = Staff.objects.filter(group__name="Administrator")

    return render_to_response('company/list.html', locals(), context_instance=RequestContext(request))

def company_detail(request):
    if request.session["user"]["group"] != "Super Administrator":
        return HttpResponseForbidden()

    staff = Staff.objects.get(pk=request.GET["id"])
    phones_tp = Phone_Company.objects.filter(company=staff.company)
    phones = {phone.type: phone.phone for phone in phones_tp}

    partners, clerks, partner_qualifications = staff.company.partner.split("@@@"), staff.company.la_clerk.split("@@@"), \
                        staff.company.partner_qualification.split("@@@")
    try:
        phone_personal = Phone.objects.filter(contact=staff.contact, type="personal")[0].phone
    except:
        phone_personal = ""

    return render_to_response('company/detail.html', locals(), context_instance=RequestContext(request))

@login_required()
def verification(request):
    staff = Staff.objects.get(group_id=request.session["user"]["group_id"], \
                company_id=request.session["user"]["company_id"])

    if staff.email_verification == "-1":
        return redirect("/matter/list")
    else:
        if request.GET:
            if staff.email_verification == request.GET['code']:
                staff.email_verification = "-1"
                staff.save()
                return redirect("/matter/list")

    return render_to_response('verification.html', locals(), context_instance=RequestContext(request))

@login_required()
def project_list(request):
    projects = Project.objects.all()

    return render_to_response('project/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def project_remove(request):
    Project.objects.get(pk=request.GET["id"]).delete()
    projects = Project.objects.all()
    return render_to_response('project/_list.html', locals(), context_instance=RequestContext(request))

@login_required()
def property_template(request):
    template = Contact_Template.objects.get(type="template_property_denning")
    template.json = request.GET["json"]
    template.save()

    return HttpResponse(str(template.id))

@login_required()
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

@login_required()
def mukim_list(request):
    mukims = Mukim.objects.all()
    return render_to_response('mukim/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def mukim_remove(request):
    Mukim.objects.get(pk=request.GET['id']).delete()
    return render_to_response('mukim/_list.html', locals(), context_instance=RequestContext(request))

def forgot_password(request):
    staff = Staff.objects.filter(login_id=request.GET["email"])
    if len(staff) > 0:
        staff[0].change_password = getRandomDigits(15)
        staff[0].save()

        url = "http://%s:%s/change_password/%d/?token=%s" % (request.META["SERVER_NAME"], request.META["SERVER_PORT"], staff[0].id, staff[0].change_password)
        body = "Please change password: <a href='%s'>%s</a>" % (url, url)
        send_email(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.DEFAULT_FROM_EMAIL, \
                  request.GET["email"], "Change password", body)
    else:
        return HttpResponse("False")

    return HttpResponse("True")

def change_password(request, id):
    if "token" not in request.GET and ('user' not in request.session or request.session['user'] is None):
        return HttpResponseForbidden()

    login = ('user' in request.session and request.session['user'] is not None)
    staff = Staff.objects.get(pk=id)
    if (login or staff.change_password != "-1") and request.POST:
        if login or request.POST["token"] == staff.change_password:
            staff.change_password = "-1"
            staff.password = md5.new(request.POST['password']).hexdigest()
            staff.save()

            return redirect("/login")

    elif login or (staff.change_password != "-1" and staff.change_password == request.GET["token"]):
        token = request.GET["token"] if "token" in request.GET else ""
        return render_to_response('change_password.html', locals(), context_instance=RequestContext(request))

    return HttpResponseForbidden()

def getRandomDigits(length):
    return ''.join(["%s" % random.randint(0, 9) for num in range(0, length)])

