from django.conf.urls import url

from project import views

urlpatterns = [
    url(r'^$', views.property, name="property"),
    url(r'^matter-code$', views.matterCode, name="matter-code"),
    url(r'^contact$', views.contact, name="matter-code"),
    url(r'^kjl$', views.kjl, name="kjl"),
]

