
from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.users import Users

class EligibleCollabtors(APIView):
    
    def post(self, request):
        active_user = request.session['email_id'] 
        users = Users.objects.filter(active = True, email_verified = True).exclude(email = active_user)
        result = []
        for user in users:
            result.append({
                "name" : user.name,
                "email" : user.email
            })
        return HttpUtil.respond(200, None, result)