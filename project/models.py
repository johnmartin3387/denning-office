from __future__ import unicode_literals

from django.db import models

class Contact_Info(models.Model):
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    address3 = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    mail_preference = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Contact_Info'

class Contact_Template(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    json = models.TextField(blank=True, null=True, default="{}")

    class Meta:
        db_table = 'Contact_Template'

    def __unicode__(self):
        return "%s" % self.type

class Contact(models.Model):
    id_type = models.ForeignKey('Attribute', blank=True, null=True, related_name="id_type")
    id_value = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.ForeignKey('Attribute', blank=True, null=True, related_name="title")
    citizenship = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    info = models.ForeignKey('Contact_Info', blank=True, null=True)
    gst_reg_no = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Contact'

    def __unicode__(self):
        return "%s" % self.title

'''class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    info = models.ForeignKey('Contact_Info', blank=True, null=True)

    class Meta:
        db_table = 'Address'

    def __unicode__(self):
        return "%s" % self.street'''

class Phone(models.Model):
    phone = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    contact = models.ForeignKey('Contact', blank=True, null=True)

    class Meta:
        db_table = 'Phone'

    def __unicode__(self):
        return "%s" % self.phone

class Phone_Company(models.Model):
    phone = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey('Company', blank=True, null=True)

    class Meta:
        db_table = 'Phone_Company'

    def __unicode__(self):
        return "%s" % self.phone

'''class Privilege(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        db_table = 'Privilege'

    def __unicode__(self):
        return "%s" % self.name'''

class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey('Company', blank=True, null=True)
    # parent = models.ForeignKey('self', blank=True, null=True)
    privilege_json = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Group'

    def __unicode__(self):
        return "%s" % self.name

'''class Grant(models.Model):
    group = models.ForeignKey('Group', blank=True, null=True)
    privilege = models.ForeignKey('Privilege', blank=True, null=True)

    class Meta:
        db_table = 'Grant'''

class Company(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    initials = models.CharField(max_length=255, blank=True, null=True)
    description1 = models.ForeignKey('Attribute', blank=True, null=True, related_name="description1")
    description2 = models.ForeignKey('Attribute', blank=True, null=True, related_name="description2")
    info = models.ForeignKey('Contact_Info', blank=True, null=True)
    phone1 = models.CharField(max_length=255, blank=True, null=True)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    phone3 = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    fax2 = models.CharField(max_length=255, blank=True, null=True)
    commencement_date = models.DateField(blank=True, null=True)

    gst_registered = models.BooleanField(default=True)
    gst_rate = models.FloatField(blank=True, default=0, null=True)
    registration_no = models.CharField(max_length=255, blank=True, null=True)
    register_date = models.DateField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    taxable_period = models.IntegerField(blank=True, default=3, null=True) # month 

    partner_label = models.CharField(max_length=255, blank=True, null=True)
    partner = models.TextField(null=True, blank=True, default="")
    partner_qualification = models.TextField(null=True, blank=True, default="")
    la_label = models.CharField(max_length=255, blank=True, null=True)
    la_clerk = models.TextField(null=True, blank=True, default="")

    tax_invoice = models.TextField(null=True, blank=True, default="")
    quotation = models.TextField(null=True, blank=True, default="")
    receipt = models.TextField(null=True, blank=True, default="")
    message = models.TextField(null=True, blank=True, default="")

    class Meta:
        db_table = 'Company'

class Staff(models.Model):
    contact = models.ForeignKey('Contact', blank=True, null=True)
    login_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    marital = models.BooleanField(default=False)
    spouse_name = models.CharField(max_length=255, blank=True, null=True)
    number_children = models.IntegerField(blank=True, default=0, null=True)
    qualification = models.ForeignKey('Attribute', blank=True, null=True, related_name="qualification")
    department = models.ForeignKey('Attribute', blank=True, null=True, related_name="department_staff")
    position_type = models.ForeignKey('Attribute', blank=True, null=True, related_name="position_type")
    monthly_salary = models.IntegerField(blank=True, default=0, null=True)
    prev_adjustment_date = models.DateField(blank=True, null=True)
    annual_leave = models.IntegerField(blank=True, default=0, null=True)
    date_commenced = models.DateField(blank=True, null=True, default=None)
    date_ceased = models.DateField(blank=True, null=True, default=None)
    tenure_employed = models.ForeignKey('Attribute', blank=True, null=True, related_name="tenure")
    status = models.CharField(max_length=255, blank=True, null=True)
    tax_file_no = models.IntegerField(blank=True, default=0, null=True)
    socso_no = models.IntegerField(blank=True, default=0, null=True)
    epf_no = models.IntegerField(blank=True, default=0, null=True)
    remarks = models.TextField(null=True, blank=True)
    company = models.ForeignKey('Company', blank=True, null=True)
    group = models.ForeignKey('Group', blank=True, null=True)

    email_verification = models.CharField(max_length=255, blank=True, null=True)
    change_password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Staff'

    def __unicode__(self):
        return "%s" % self.nickname

class Normal(models.Model):
    contact = models.ForeignKey('Contact', blank=True, null=True)
    # privilege = models.ForeignKey('Privilege', blank=True, null=True)
    old_ic = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    registered_office = models.CharField(max_length=255, blank=True, null=True)
    directors = models.CharField(max_length=255, blank=True, null=True)
    secretary = models.ForeignKey('Contact', blank=True, null=True, related_name="secretary")
    template = models.ForeignKey('Contact_Template', blank=True, null=True)

    class Meta:
        db_table = 'Normal'

class Checklist(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Checklist'

    def __unicode__(self):
        return "%s" % self.code

class Matter_Code(models.Model):
    related = models.ForeignKey('self', blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    matter_tp = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Attribute', blank=True, null=True, related_name="category")
    department = models.ForeignKey('Attribute', blank=True, null=True, related_name="department")
    turnaround = models.IntegerField(blank=True, default=0, null=True)
    billing_code = models.CharField(max_length=255, blank=True, null=True)
    favourites = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True, null=True, default="[]")
    checklist = models.ForeignKey('Checklist', blank=True, null=True)

    class Meta:
        db_table = 'Matter_Code'

    def __unicode__(self):
        return "%s" % self.code

class Matter(models.Model):
    checklist = models.ForeignKey('Checklist', blank=True, null=True)
    file_number = models.CharField(max_length=255, blank=True, null=True)
    file_number2 = models.CharField(max_length=255, blank=True, null=True)
    open_date = models.DateField(blank=True, null=True)
    status = models.ForeignKey('Attribute', blank=True, null=True)
    related = models.ForeignKey('self', blank=True, null=True)
    pocket_location = models.CharField(max_length=255, blank=True, null=True)
    physical_location = models.CharField(max_length=255, blank=True, null=True)
    box_location = models.CharField(max_length=255, blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    turnaround = models.IntegerField(blank=True, default=0, null=True)
    billing_code = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    matter_code = models.ForeignKey('Matter_Code', blank=True, null=True)
    primary_client = models.ForeignKey('Normal', blank=True, null=True, related_name="primary_client")
    la_in_charge = models.ForeignKey('Staff', blank=True, null=True, related_name="la_in_charge")
    clerk_in_charge = models.ForeignKey('Staff', blank=True, null=True, related_name="clerk_in_charge")
    partner_in_charge = models.ForeignKey('Staff', blank=True, null=True, related_name="partner_in_charge")

    class Meta:
        db_table = 'Matter'

class Matter_Contact(models.Model):
    matter = models.ForeignKey('Matter', blank=True, null=True)
    contact = models.ForeignKey('Contact', blank=True, null=True)

    class Meta:
        db_table = 'Matter_Contact'

class Attribute(models.Model):
    value = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Attribute'

    def __unicode__(self):
        return "%s" % self.value

class Task(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    after = models.CharField(max_length=255, blank=True, null=True)
    est_time = models.DateTimeField(blank=True, null=True)
    due_time = models.DateTimeField(blank=True, null=True)
    done_time = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    checklist = models.ForeignKey('Checklist', blank=True, null=True)

    class Meta:
        db_table = 'Task'

    def __unicode__(self):
        return "%s" % self.code

class Template(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    matter = models.ForeignKey('Matter', blank=True, null=True)
    task = models.ForeignKey('Task', blank=True, null=True)

    class Meta:
        db_table = 'Template'

    def __unicode__(self):
        return "%s" % self.name

class Project(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    phase = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    license_no = models.CharField(max_length=255, blank=True, null=True)
    license_date = models.CharField(max_length=255, blank=True, null=True)
    # license_expiry_date = models.DateTimeField(blank=True, null=True)
    permit_no = models.CharField(max_length=255, blank=True, null=True)
    permit_commencement_date = models.DateTimeField(blank=True, null=True)
    permit_expiry_date = models.DateTimeField(blank=True, null=True)
    approval = models.CharField(max_length=255, blank=True, null=True)
    local_authority = models.ForeignKey('Attribute', blank=True, null=True, related_name="local_authority")
    complete_date = models.DateTimeField(blank=True, null=True)
    encumbrances = models.ForeignKey('Normal', blank=True, null=True, related_name="encumbrances")
    land_tenure = models.ForeignKey('Attribute', blank=True, null=True, related_name="land_tenure")
    lease_expiry_date = models.DateTimeField(blank=True, null=True)
    note1 = models.CharField(max_length=255, blank=True, null=True)
    note2 = models.CharField(max_length=255, blank=True, null=True)
    developer = models.ForeignKey('Normal', blank=True, null=True, related_name="developer")
    proprietor = models.ForeignKey('Normal', blank=True, null=True, related_name="proprietor")
    bank = models.ForeignKey('Normal', blank=True, null=True, related_name="bank")
    hda_no = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Project'

    def __unicode__(self):
        return "%s" % self.name


class Mukim(models.Model): 
    mukim = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Mukim'   

    def __unicode__(self):
        return "%s" % self.mukim

class Property(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    individual = models.BooleanField(default=True)
    title_type = models.ForeignKey('Attribute', blank=True, null=True, related_name="title_type")
    title_no = models.CharField(max_length=255, blank=True, null=True)
    lot_type = models.ForeignKey('Attribute', blank=True, null=True, related_name="lot_type")
    lot_no = models.CharField(max_length=255, blank=True, null=True)
    mukim = models.CharField(max_length=255, blank=True, null=True)
    mukim_val = models.ForeignKey('Mukim', blank=True, null=True)
    daerah = models.CharField(max_length=255, blank=True, null=True)
    negeri = models.CharField(max_length=255, blank=True, null=True)
    area = models.IntegerField(blank=True, default=0, null=True)
    area_unit = models.CharField(max_length=255, blank=True, null=True)
    tenure = models.ForeignKey('Attribute', blank=True, null=True, related_name="property_tenure")
    lease_expiry_date = models.DateTimeField(blank=True, null=True)
    title_registeration_date = models.DateTimeField(blank=True, null=True)
    interest = models.BooleanField(default=False)
    buml_lot = models.BooleanField(default=False)
    malay = models.BooleanField(default=False)
    restriction_against = models.ForeignKey('Attribute', blank=True, null=True, related_name="restriction_against")
    approving_authority = models.ForeignKey('Attribute', blank=True, null=True, related_name="approving_authority")
    other_restriction = models.ForeignKey('Attribute', blank=True, null=True, related_name="other_restriction")
    category_land_use = models.ForeignKey('Attribute', blank=True, null=True, related_name="category_land_use")
    express_condition = models.ForeignKey('Attribute', blank=True, null=True, related_name="express_condition")
    building_type = models.ForeignKey('Attribute', blank=True, null=True, related_name="building_type")
    building_age = models.CharField(max_length=255, blank=True, null=True)
    postal_address = models.CharField(max_length=255, blank=True, null=True)
    assessment_rate = models.FloatField(blank=True, default=0, null=True)
    annual_quit_rent = models.FloatField(blank=True, default=0, null=True)
    previous_title = models.CharField(max_length=255, blank=True, null=True)

    parcel_no = models.CharField(max_length=255, blank=True, null=True)
    storey_no = models.CharField(max_length=255, blank=True, null=True)
    building_no = models.CharField(max_length=255, blank=True, null=True)
    access_parcel_no = models.CharField(max_length=255, blank=True, null=True)
    access_storey_no = models.CharField(max_length=255, blank=True, null=True)
    access_building_no = models.CharField(max_length=255, blank=True, null=True)
    unit_of_share = models.CharField(max_length=255, blank=True, null=True)
    total_share = models.CharField(max_length=255, blank=True, null=True)
    floor_area = models.CharField(max_length=255, blank=True, null=True)

    pacel_spa_no = models.CharField(max_length=255, blank=True, null=True)
    pacel_spa_value = models.CharField(max_length=255, blank=True, null=True)
    story_no_spa = models.CharField(max_length=255, blank=True, null=True)
    block_no = models.CharField(max_length=255, blank=True, null=True)
    apt_name = models.CharField(max_length=255, blank=True, null=True)
    access_parcel_no_spa = models.CharField(max_length=255, blank=True, null=True)
    building_description = models.ForeignKey('Attribute', blank=True, null=True, related_name="building_description")
    spa_area = models.IntegerField(blank=True, default=0, null=True)
    spa_area_unit = models.CharField(max_length=255, blank=True, null=True)

    project = models.ForeignKey('Project', blank=True, null=True)
    master_title = models.TextField(blank=True, null=True)

    additional_info = models.TextField(blank=True, null=True)
    template = models.ForeignKey('Contact_Template', blank=True, null=True)

    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'Property'   

    def __unicode__(self):
        return "%s" % self.name

    