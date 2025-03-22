import uuid
from django.db import models
from django.utils.timezone import now

class Users(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    verification_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    create_time = models.DateTimeField(default=now)
    
    class Meta:
        db_table = 'users'