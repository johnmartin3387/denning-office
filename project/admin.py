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