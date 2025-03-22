from src.util.regex import validate_and_format_email
from rest_framework.decorators import api_view
from src.models.credentials import Credentials
from src.util.http_util import HttpUtil
from src.models.users import Users

@api_view(['POST'])
def update_user_info(request, email):
    data = request.data
    errors = []
    try:   
        email_id = validate_and_format_email(email)
        if(email_id == '' or email_id == None):
            errors.append('Email ID cannot be empty')
        
        user = Users.objects.get(email = email)

        name = data.get('name', None)
        if(name != None and name != ''):
            user.name = name

        password = data.get('password', None)
        if(password != None and password != ''):
            if(user.credentials == None):
                user.credentials = Credentials()
            user.credentials.password = password

        return HttpUtil.respond(201, "Success", None)
        
    except Exception as e0: 
        return HttpUtil.respond(500, str(e0))