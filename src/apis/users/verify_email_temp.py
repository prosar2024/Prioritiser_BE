from rest_framework.views import APIView
from django.shortcuts import render
from src.models.users import Users
from django.conf import settings


class VerifyEmailTemp(APIView):

    def get(self, request, email):
        try:
            print(email)
            users = Users.objects.filter(email=email)
            if(not users.exists()):
                content = {
                    'icon' : 'error',
                    'title' : 'Email Verification Failed',
                    'body' : 'Oops, We couldn\'t recognize this email ID'
                }
            else:
                user = users.first()
                if(not user.active):
                    content = {
                        'icon' : 'error',
                        'title' : 'Email Verification Failed',
                        'body' : 'This account is inactive. Please contact system admin.'
                    }
                else:    
                    if(user.email_verified):
                        content = {
                            'icon' : 'info',
                            'title' : 'Account Already Verified',
                            'body' : 'Hello <b>{}</b>, <br><br>Your email has been already verified. <br>You can access all features of Prosar Prioritiser.'.format(user.name)
                        }
                    else:
                        user.email_verified = True
                        user.verification_uuid = None
                        user.save()
                        content = {
                            'icon' : 'success',
                            'title' : 'Email Verification Successful',
                            'body' : 'Hello <b>{}</b>, <br><br>Your email has been successfully verified. <br>You can now access all features of Prosar Prioritiser.'.format(user.name)
                        }
        except:
            content = {
                'icon' : 'error',
                'title' : 'Email Verification Failed',
                'body' : 'Oops, Something failed in between. Please contact system admin if the issue persists.'
            }
        
        content['login_page_url'] = settings.FRONTEND_URL+"/login"
        return render(request, "email_verification_confirmation_template.html", content)