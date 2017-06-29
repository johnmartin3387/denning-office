from django.conf.urls import url

from project import views

urlpatterns = [
    url(r'property/update$', views.property_update, name="property_edit"),
    url(r'property/list$', views.property_list, name="property_list"),
    url(r'property/remove$', views.property_remove, name="property_remove"),

    url(r'matter-code/update$', views.matterCode_update, name="mattercode_edit"),
    url(r'matter-code/list$', views.matterCode_list, name="mattercode_list"),
    url(r'matter-code/remove$', views.matterCode_remove, name="mattercode_remove"),

    url(r'contact/update$', views.contact_update, name="contact_edit"),
    url(r'contact/list$', views.contact_list, name="contact_list"),
    url(r'contact/remove$', views.contact_remove, name="contact_remove"),

    url(r'matter/update$', views.matter_update, name="matter_edit"),
    url(r'matter/list$', views.matter_list, name="matter_list"),
    url(r'matter/remove$', views.matter_remove, name="matter_remove"),

    url(r'staff/update$', views.staff_update, name="staff_edit"),
    url(r'staff/list$', views.staff_list, name="staff_list"),
    url(r'staff/remove$', views.staff_remove, name="staff_remove"),

    url(r'project/update$', views.project_update, name="project_edit"),
    url(r'project/list$', views.project_list, name="project_list"),
    url(r'project/remove$', views.project_remove, name="project_remove"),

    url(r'mukim/update$', views.mukim_update, name="mukim_edit"),
    url(r'mukim/list$', views.mukim_list, name="mukim_list"),
    url(r'mukim/remove$', views.mukim_remove, name="mukim_remove"),

    url(r'states$', views.states, name="states")
]
