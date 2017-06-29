
from django.core.exceptions import ObjectDoesNotExist
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, Authentication, SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized, NotFound
from tastypie.cache import SimpleCache, NoCache
from tastypie.paginator import Paginator

from project.models import *

class CustomAuthorization(Authorization):
    def create_list(self, object_list, bundle): 
        return True

    def create_detail(self, object_list, bundle):
        return True

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        return True

    def update_detail(self, object_list, bundle):
        return True

    def delete_list(self, object_list, bundle):
        return True

    def delete_detail(self, object_list, bundle):
        return True

    def put_detail(self, object_list, bundle):
        return True

class DjangoCookieBasicAuthentication(BasicAuthentication):
    """
     If the user is already authenticated by a django session it will
     allow the request (useful for ajax calls) . If it is not, defaults
     to basic authentication, which other clients could use.
    """

    def __init__(self, *args, **kwargs):
        super(DjangoCookieBasicAuthentication, self).__init__(*args, **kwargs)

    def is_authenticated(self, request, **kwargs):
        # print ("is auth")

        # from django.contrib.sessions.models import Session
        # if 'sessionid' in request.COOKIES:
        #     try:
        #         s = Session.objects.get(pk=request.COOKIES['sessionid'])
        #         if '_auth_user_id' in s.get_decoded():
        #             u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
        #             request.user = u
        #             print "user logged in using session"
        #             return True
        #     except:
        #         print "session not exist",request.COOKIES['sessionid']
        # if 'HTTP_token' in request.META:
        #     s = Session.objects.get(pk=request.META['HTTP_token'])
        #     if '_auth_user_id' in s.get_decoded():
        #         u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
        #         request.user = u
        #         return True

        # result=super(DjangoCookieBasicAuthentication, self).is_authenticated(request, **kwargs)
        result = request.user.is_authenticated()
        # return result
        return True

    def get_identifier(self, request):
        return request.user

class ContactInfoResource(ModelResource):
    class Meta:
        queryset = Contact_Info.objects.all()
        resource_name = 'contact_info'
        allowed_methods = ['get', 'post']
        # authentication = DjangoCookieBasicAuthentication()
        # authorization = CustomAuthorization()

        filtering = {
            'id': ALL
        }

class ContactResource(ModelResource):
    class Meta:
        queryset = Contact.objects.all().exclude(type="staff")
        resource_name = 'contact'
        allowed_methods = ['get', 'put', 'post']
        authentication = DjangoCookieBasicAuthentication()
        authorization = CustomAuthorization()

        filtering = {
            'id': ALL,
        }

class ContactTemplateResource(ModelResource):
    class Meta:
        queryset = Contact_Template.objects.all()
        resource_name = 'contact_template'
        allowed_methods = ['get', 'put', 'post']
        authentication = DjangoCookieBasicAuthentication()
        authorization = CustomAuthorization()

        filtering = {
            'id': ALL,
            'type': ALL_WITH_RELATIONS,
        }

class AttributeResource(ModelResource):
    class Meta:
        queryset = Attribute.objects.all()
        resource_name = 'attribute'
        allowed_methods = ['get', 'put', 'post']
        authentication = DjangoCookieBasicAuthentication()
        authorization = CustomAuthorization()

        filtering = {
            'id': ALL,
            'type': ALL_WITH_RELATIONS,
        }

class MatterCodeResource(ModelResource):
    class Meta:
        queryset = Matter_Code.objects.all()
        resource_name = 'matter_code'
        allowed_methods = ['get', 'put', 'post']
        authentication = DjangoCookieBasicAuthentication()
        authorization = CustomAuthorization()

        filtering = {
            'id': ALL
        }

class MatterResource(ModelResource):
    class Meta:
        queryset = Matter.objects.all()
        resource_name = 'matter'
        allowed_methods = ['get', 'put', 'post']
        authentication = DjangoCookieBasicAuthentication()
        authorization = CustomAuthorization()

        filtering = {
            'id': ALL
        }
