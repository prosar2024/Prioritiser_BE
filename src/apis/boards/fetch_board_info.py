from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.boards import Boards
import uuid

class FetchBoardInfo(APIView):
    
    def get(self, request, board_id):
        try:
            active_user = request.session['email_id'] 
            board = Boards.objects.get(board_id=uuid.UUID(board_id))

            collaborators = []
            owner_name = None
            owner_email = None

            for c in board.collaborators.all():
                if c.owner:
                    owner_name = c.user.name
                    owner_email = c.user.email

                collaborators.append({
                    "name": c.user.name,
                    "email": c.user.email,
                    "owner": c.owner,
                    "accepted": c.accepted
                })

            result = {
                "board_id": board.board_id,
                "name": board.name,
                "description": board.description,
                "owner_name": owner_name,
                "owner_email": owner_email,
                "created_on": board.created_time,
                "collaborators": collaborators
            }

            return HttpUtil.respond(200, None, result)
        except Exception as e0:
            return HttpUtil.respond(500, str(e0))
