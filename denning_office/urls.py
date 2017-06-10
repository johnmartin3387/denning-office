from django.conf.urls import url, include

from django.contrib import admin
from project import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('project.urls')),
    url(r'^api/', include('api.urls')),
]

