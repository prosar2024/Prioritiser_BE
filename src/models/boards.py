from django.db import models
import uuid

class Boards(models.Model):
    board_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    retired = models.BooleanField(default=False)
    summary = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'boards'