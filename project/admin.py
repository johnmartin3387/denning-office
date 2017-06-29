from django.contrib import admin
from .models import *

class ContactInfoAdmin(admin.ModelAdmin):
    model = Contact_Info
    list_display = ['id', 'country', 'state', 'town', 'website']
    list_display_links = ['id']

admin.site.register(Contact_Info, ContactInfoAdmin)

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ['id', 'type', 'id_type', 'name', 'title']
    list_display_links = ['id']

admin.site.register(Contact, ContactAdmin)

class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    list_display = ['id', 'type', 'value']
    list_display_links = ['id']

admin.site.register(Attribute, AttributeAdmin)

class NormalAdmin(admin.ModelAdmin):
    model = Normal
    list_display = ['id']
    list_display_links = ['id']

admin.site.register(Normal, NormalAdmin)

class StaffAdmin(admin.ModelAdmin):
    model = Staff
    list_display = ['id', 'login_id']
    list_display_links = ['id', 'login_id']

admin.site.register(Staff, StaffAdmin)

class PhoneAdmin(admin.ModelAdmin):
    model = Phone
    list_display = ['id']
    list_display_links = ['id']

admin.site.register(Phone, PhoneAdmin)

class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['id']
    list_display_links = ['id']

admin.site.register(Project, ProjectAdmin)

class ContactTemplateAdmin(admin.ModelAdmin):
    model = Contact_Template
    list_display = ['id']
    list_display_links = ['id']

admin.site.register(Contact_Template, ContactTemplateAdmin)

class MatterAdmin(admin.ModelAdmin):
    model = Matter
    list_display = ['id']
    list_display_links = ['id']

admin.site.register(Matter, MatterAdmin)

