from django.db import models
from src.models.users import Users
from src.models.boards import Boards
from rest_framework import serializers
from src.models.users import Users
from src.models.boards import Boards

class Collaborators(models.Model):
    board = models.ForeignKey(Boards, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    retired = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.board.name}"
    
    class Meta:
        db_table = 'collaborators'


class CollaboratorsSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Collaborators
        fields = ['user_email', 'creation_time', 'accepted', 'retired', 'owner']

    def validate_user(self, value):
        if not Users.objects.filter(email=value.email, active = True).exists():
            raise serializers.ValidationError("User with email '{}' does not exist or is not active.".format(value.email))
        return value
