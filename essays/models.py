from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Essay(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, 
                          default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)
    submitted_at = models.DateTimeField(auto_now_add=True)


