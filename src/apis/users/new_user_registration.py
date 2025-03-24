from src.util.regex import validate_and_format_email
from django.template.loader import render_to_string
from src.models.credentials import Credentials
from src.util.email_util import EmailUtil
from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.users import Users
from django.db import transaction
import os

class NewUserRegistration(APIView):

    def post(self, request):
        data = request.data
        errors = []
        try:   
            with transaction.atomic():
                email_id = validate_and_format_email(data.get('email', None))
                if(email_id == '' or email_id == None):
                    errors.append('Email ID cannot be empty')
                else:
                    if(Users.objects.filter(email = email_id).exists()):
                        return HttpUtil.respond(400, {"Email ID is already registered"}, None)
                        
                name = data.get('name', None)
                if(name == None or name == ''):
                    errors.append("Name cannot be empty")
                elif(len(name) < 3):
                    errors.append("Name must have atleast 3 chars.")
                
                password = data.get('password', None)
                if(password == None or password == ''):
                    errors.append("Password cannot be empty")
                elif(len(password) < 8):
                    errors.append("Password must be atleast 8 chars long")

                if(not errors):
                    user = Users()
                    user.email = email_id
                    user.name = name.strip()
                    user.save()

                    credential = Credentials()
                    credential.user = user
                    credential.password = password.strip()
                    credential.save()
                    
                    #Handle Email
                    verification_link = request.build_absolute_uri(f"/api/users/verify/{user.email}/{user.verification_uuid}/")
                    body = render_to_string("verify_email_template.html", {"name": user.name, "verification_link": verification_link})
                    subject = "Verify Your Email - Prosar Prioritiser"
                    EmailUtil.send(to_email = user.email, subject = subject, body = body)

                    return HttpUtil.respond(201, "Success", {"email" : email_id})
                else:
                    return HttpUtil.respond(400, errors, None)
            
        except Exception as e0: 
            raise e0
            return HttpUtil.respond(500, str(e0))