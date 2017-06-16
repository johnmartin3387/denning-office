from django.conf.urls import url

from project import views

urlpatterns = [
    url(r'^property/update$', views.property_update, name="property_edit"),
    url(r'^property/list$', views.property_list, name="property_list"),

    url(r'^matter-code/update$', views.matterCode_update, name="mattercode_edit"),
    url(r'^matter-code/list$', views.matterCode_list, name="mattercode_list"),
    url(r'^matter-code/remove$', views.matterCode_remove, name="mattercode_remove"),

    url(r'^contact/update$', views.contact_update, name="contact_edit"),
    url(r'^contact/list$', views.contact_list, name="contact_list"),
    url(r'^contact/remove$', views.contact_remove, name="contact_remove"),
]

