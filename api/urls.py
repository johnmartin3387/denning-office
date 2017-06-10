from django.conf.urls import patterns, include, url

from api.api_func import *
from project import views

urlpatterns = [
    url(r'^', include(ContactInfoResource().urls)),
]

