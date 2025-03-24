from django.template.loader import render_to_string
from src.models.collaborators import Collaborators
from src.util.email_util import EmailUtil
from rest_framework.views import APIView
from src.util.http_util import HttpUtil
from src.models.boards import Boards
from src.models.users import Users
from django.db import transaction
import uuid

class UpdateBoard(APIView):

    def post(self, request):
        with transaction.atomic():
            data = request.data
            active_user = request.session['email_id']
            board_id = uuid.UUID(data.get("board_id"))

            name = data.get("name")
            description = data.get("description")
            new_collaborators = set(data.get("collaborators", []))  # incoming list
            invalid_users = []

            if not name:
                return HttpUtil.respond(400, "Board name is required.")
            
            try:
                board = Boards.objects.get(board_id=board_id)
            except Boards.DoesNotExist:
                return HttpUtil.respond(404, "Board not found.")

            # Update board info
            board.name = name
            board.description = description
            board.summary = description or ""
            board.save()

            # Ensure owner is in system
            try:
                owner = Users.objects.get(email=active_user)
            except Users.DoesNotExist:
                return HttpUtil.respond(400, "Active user not found.")

            # Get current collaborators (excluding owner)
            existing_collabs = Collaborators.objects.filter(board=board, owner=False)
            existing_emails = set(existing_collabs.values_list("user__email", flat=True))

            # Determine who to remove and who to add
            to_remove = existing_emails - new_collaborators
            to_add = new_collaborators - existing_emails - {active_user}

            # Delete removed collaborators
            Collaborators.objects.filter(
                board=board,
                user__email__in=to_remove
            ).delete()

            # Add new collaborators
            for email in to_add:
                try:
                    user = Users.objects.get(email=email, active=True, email_verified=True)
                    Collaborators.objects.create(board=board, user=user)
                    #Handle Email
                    body = render_to_string("board_collaboration_invite.html", {"name": user.name, "board": name, "owner" : owner.name})
                    subject = "Collaborator"
                    EmailUtil.send(to_email = user.email, subject = subject, body = body)
                except Users.DoesNotExist:
                    invalid_users.append(f"Failed to add: {email}")

            return HttpUtil.respond(200, invalid_users, {"board_id": board.board_id})
