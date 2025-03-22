from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.users import Users

class GetUserInfo(APIView):

    def get(self, request):
        try:   
            email_id = request.session['email_id']
            user = Users.objects.get(email = email_id)
            data = {
                "email" : user.email, 
                "name" : user.name,
                "active" : user.active,
                "email_verified" : user.email_verified,
                "verification_uuid" : user.verification_uuid,
                "create_time" : user.create_time,
                "failed_login_count" : user.credentials.failed_login_count,
                "last_logged_in_time" : user.credentials.last_logged_in_time,
                "locked" : user.credentials.locked
            }
            return HttpUtil.respond(200, "Success", data)
            
        except Exception as e0: 
            return HttpUtil.respond(500, str(e0))