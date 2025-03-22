from django.db import models
from rest_framework import serializers
from src.models.boards import Boards
from src.models.collaborators import CollaboratorsSerializer
import uuid

class Boards(models.Model):
    board_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'boards'

class BoardSerializer(serializers.ModelSerializer):
    collaborators = CollaboratorsSerializer(many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ['board_id', 'name', 'description', 'created_time', 'summary', 'collaborators']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name field cannot be empty or whitespace.")
        return value
