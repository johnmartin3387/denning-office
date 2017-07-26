from django.conf.urls import patterns, include, url

from api.api_func import *
from project import views

urlpatterns = [
    url(r'^', include(ContactInfoResource().urls)),
    url(r'^', include(ContactTemplateResource().urls)),
    url(r'^', include(AttributeResource().urls)),
    url(r'^', include(MatterCodeResource().urls)),
    url(r'^', include(ContactResource().urls)),
    url(r'^', include(GroupResource().urls)),
    url(r'^', include(CompanyResource().urls)),

    url(r'update_property_template', views.property_template, name="property_template")
]

