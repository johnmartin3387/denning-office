from __future__ import unicode_literals

from django.db import models

class Contact_Info(models.Model):
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

class Contact(models.Model):
    id_type = models.IntegerField(blank=True, default=0, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    citizenship = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    info = models.ForeignKey('Contact_Info', blank=True, null=True)

    class Meta:
        db_table = 'Contact'

    def __unicode__(self):
        return "%s" % self.title

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    info = models.ForeignKey('Contact_Info', blank=True, null=True)

    class Meta:
        db_table = 'Address'

    def __unicode__(self):
        return "%s" % self.street

class Phone(models.Model):
    phone = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    info = models.ForeignKey('Contact_Info', blank=True, null=True)

    class Meta:
        db_table = 'Phone'

    def __unicode__(self):
        return "%s" % self.phone

class Privilege(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        db_table = 'Privilege'

    def __unicode__(self):
        return "%s" % self.title

class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        db_table = 'Group'

    def __unicode__(self):
        return "%s" % self.name

class Grant(models.Model):
    group = models.ForeignKey('Group', blank=True, null=True)
    privilege = models.ForeignKey('Privilege', blank=True, null=True)

    class Meta:
        db_table = 'Grant'

class Staff(models.Model):
    contact = models.ForeignKey('Contact', blank=True, null=True)
    login_id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    marital = models.BooleanField(default=False)
    spouse_name = models.CharField(max_length=255, blank=True, null=True)
    number_children = models.IntegerField(blank=True, default=0, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    position_type = models.CharField(max_length=255, blank=True, null=True)
    monthly_salary = models.IntegerField(blank=True, default=0, null=True)
    prev_adjustment_date = models.DateTimeField(blank=True, null=True)
    annual_leave = models.IntegerField(blank=True, default=0, null=True)
    date_commenced = models.DateTimeField(blank=True, null=True)
    date_ceased = models.DateTimeField(blank=True, null=True)
    tenure_employed = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    tax_file_no = models.IntegerField(blank=True, default=0, null=True)
    socso_no = models.IntegerField(blank=True, default=0, null=True)
    epf_no = models.IntegerField(blank=True, default=0, null=True)
    remarks = models.TextField(null=True, blank=True)
    contact = models.ForeignKey('Group', blank=True, null=True)

    class Meta:
        db_table = 'Staff'

    def __unicode__(self):
        return "%s" % self.nickname

class Normal(models.Model):
    contact = models.ForeignKey('Contact', blank=True, null=True)
    privilege = models.ForeignKey('Privilege', blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    old_ic = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Normal'

    def __unicode__(self):
        return "%s" % self.email

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
    category = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    turnaround = models.IntegerField(blank=True, default=0, null=True)
    billing_code = models.CharField(max_length=255, blank=True, null=True)
    favourites = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True, null=True)
    checklist = models.ForeignKey('Checklist', blank=True, null=True)

    class Meta:
        db_table = 'Matter_Code'

    def __unicode__(self):
        return "%s" % self.code

class Matter(models.Model):
    checklist = models.ForeignKey('Checklist', blank=True, null=True)
    file_number = models.CharField(max_length=255, blank=True, null=True)
    open_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    related = models.CharField(max_length=255, blank=True, null=True)
    pocket_location = models.CharField(max_length=255, blank=True, null=True)
    physical_location = models.CharField(max_length=255, blank=True, null=True)
    box_location = models.CharField(max_length=255, blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    turnaround = models.IntegerField(blank=True, default=0, null=True)
    billing_code = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    matter_code = models.ForeignKey('Matter_Code', blank=True, null=True)

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
    start_date = models.DateTimeField(blank=True, null=True)
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

class Property(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    individual = models.BooleanField(default=False)
    title_type = models.CharField(max_length=255, blank=True, null=True)
    title_no = models.CharField(max_length=255, blank=True, null=True)
    lot_type = models.CharField(max_length=255, blank=True, null=True)
    lot_no = models.CharField(max_length=255, blank=True, null=True)
    daerah = models.CharField(max_length=255, blank=True, null=True)
    negeri = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    tenure = models.CharField(max_length=255, blank=True, null=True)
    lease_expiry_date = models.DateTimeField(blank=True, null=True)
    title_registeration_date = models.DateTimeField(blank=True, null=True)
    interest = models.CharField(max_length=255, blank=True, null=True)
    restriction_against = models.CharField(max_length=255, blank=True, null=True)
    approving_authority = models.CharField(max_length=255, blank=True, null=True)
    other_restriction = models.CharField(max_length=255, blank=True, null=True)
    category_land_use = models.CharField(max_length=255, blank=True, null=True)
    express_condition = models.CharField(max_length=255, blank=True, null=True)
    building_type = models.CharField(max_length=255, blank=True, null=True)
    building_age = models.IntegerField(blank=True, default=0, null=True)
    postal_address = models.CharField(max_length=255, blank=True, null=True)
    assessment_rate = models.IntegerField(blank=True, default=0, null=True)
    annual_quit_rent = models.IntegerField(blank=True, default=0, null=True)
    previous_title = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Property'

    def __unicode__(self):
        return "%s" % self.name