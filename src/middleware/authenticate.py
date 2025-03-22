from prioritiser.settings import TOKEN_EXPIRY_TIME_IN_MINUTES
from rest_framework.renderers import JSONRenderer
from src.models.credentials import Credentials
from src.util.http_util import HttpUtil
from datetime import timedelta
from django.utils import timezone
import traceback

'''
    Authentication Middleware
'''
class Authenticate():
    excluded_urls = [
      "api/users/register/",
      "api/users/verify/",
      "api/users/authenticate/",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        full_path = request.get_full_path()
        print("ULR : {}".format(full_path))
        for excluded_url in self.excluded_urls:
            if(excluded_url in full_path):
                print("Excluding : {}".format(full_path))
                return self.get_response(request)
        
        headers = request.headers
        email = headers.get('Email', None)
        token = headers.get('Token', None)
        
        authenticated = self.__authorize(email, token)
        if(authenticated):
            request.session['email_id'] = email
            return self.get_response(request)
        else:
            response = HttpUtil.respond(401, "Authentication Failed")
            response.content_type = "application/json"
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response
 

    def __authorize(self, email, token):
        print("{} -- {}".format(email, token))
        try:
            if(token == None or token == '' or email == '' or email == None):
                return False
            time_threshold = timezone.now() - timedelta(minutes = TOKEN_EXPIRY_TIME_IN_MINUTES)
            cred = Credentials.objects.filter(user__email = email, token=token, token_generated_time__gte=time_threshold)
            if cred.exists():
                cred = cred.first()
                cred.token_generated_time = timezone.now()
                cred.save()
                return True
            else:
                return False
        except Exception as e:        
            print('Failed to authenticate [in middleware] : {}\n{}'.format(e, traceback.format_exc()))
            return False