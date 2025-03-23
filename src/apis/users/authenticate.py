from src.models.credentials import Credentials
from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from django.utils import timezone
import uuid

class Authenticate(APIView):
        
    def post(self, request):
        data = request.data
        try:   
            email = data.get('username', None)
            password = data.get('password', None)
            if(email == '' or email == None or password == '' or password == None):
                return HttpUtil.respond(400, {'Username / Password cannot be empty'})
                
            cred = Credentials.objects.get(user__email=email)
            if not cred.user.active:
                return HttpUtil.respond(400, 'User account is Inactive, please contact system admin')
            elif cred.locked:
                return HttpUtil.respond(400, 'User account us locked, please contact system admin')    
            elif not cred.user.email_verified:
                return HttpUtil.respond(400, 'Please verify your email first to login.')    
            elif(cred.password != password):
                if(cred.failed_login_count >= 3):
                    cred.locked = True
                else:
                    cred.failed_login_count = (cred.failed_login_count+1)
                return HttpUtil.respond(400, 'Incorrect Credentials')    
            else:
                cred.token = uuid.uuid4()
                cred.token_generated_time = timezone.now()
                cred.save()
                return HttpUtil.respond(200, 'Token Generated', {'token' : cred.token, 'email' : email, 'name' : cred.user.name})

        except Exception as e0: 
            return HttpUtil.respond(500, str(e0))