
from src.models.collaborators import Collaborators
from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.boards import Boards
from src.models.users import Users

class CreateNewBoard(APIView):
    
    def post(self, request):
        data = request.data
        active_user = request.session['email_id']
        name = data.get("name")
        description = data.get("description")
        collaborators = data.get("collaborators", [])
        if not name:
            return HttpUtil.respond(400, "Board name is required.")

        # Create the board
        board = Boards.objects.create(
            name=name,
            description=description,
            summary=description or ""
        )

        owner = Users.objects.get(email=active_user)
        Collaborators.objects.create(
            board=board,
            user=owner,
            owner=True,
            accepted=True
        )

        # Loop through contributor emails and add them as collaborators
        invalid_users = []
        for email in collaborators:
            if(email == active_user):
                continue
            try:
                user = Users.objects.get(email=email, active=True, email_verified = True)
                Collaborators.objects.create(
                    board=board,
                    user=user
                )
            except Users.DoesNotExist:
                invalid_users.append("Failed to add : {}".format(email))

        return HttpUtil.respond(200, invalid_users, {"board_id": board.board_id})
