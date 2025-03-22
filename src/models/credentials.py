from django.db import models
from src.models.users import Users

class Credentials(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='credentials')
    password = models.CharField(max_length=255)
    failed_login_count = models.IntegerField(default=0)
    last_logged_in_time = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=False)
    token = models.UUIDField(null=True, blank=True)
    token_generated_time = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        db_table = 'credentials'

    def __str__(self):
        return f"Credentials for {self.user.email}"

