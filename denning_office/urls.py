from django.conf.urls import url, include

from django.contrib import admin
from project import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),

    url(r'^$', views.start_page, name="start_page"),

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

    url(r'states$', views.states, name="states"),

    url(r'privilege_settings$', views.privilege_settings, name="privilege_settings"),
    url(r'login$', views.login, name="login"),
    url(r'logout$', views.logout, name="logout"),
    url(r'verification$', views.verification, name="verification"),
    url(r'forgot_password$', views.forgot_password, name="forgot_password"),
    url(r'change_password/(?P<id>[\w-]+)/$', views.change_password, name="change_password"),

    url(r'company/update$', views.company_update, name="company_edit"),
    url(r'company/list$', views.company_list, name="company_list"),
    url(r'company/detail$', views.company_detail, name="company_detail")
]

