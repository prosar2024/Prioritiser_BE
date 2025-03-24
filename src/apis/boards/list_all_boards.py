
from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.collaborators import Collaborators

class ListAllBoards(APIView):
    
    def get(self, request):
        active_user = request.session['email_id'] 
        collabs = Collaborators.objects.filter(user__email = active_user)
        result = []
        for collb in collabs:
            board = collb.board
            collaborators_qs = board.collaborators.select_related('user').all()

            collaborators = [
                {
                    "name": c.user.name,
                    "email": c.user.email,
                    "owner": c.owner,
                    "accepted": c.accepted
                }
                for c in collaborators_qs
            ]

            result.append({
                "board_id": board.board_id,
                "name": board.name,
                "description": board.description,
                "is_owner": collb.owner,
                "owner_name": next((c.user.name for c in collaborators_qs if c.owner), None),
                "created_on" : board.created_time,
                "collaborators": collaborators
            })
        return HttpUtil.respond(200, None, result)