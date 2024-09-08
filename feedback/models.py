from django.db import models
import uuid
from essays.models import Essay

# Create your models here.
class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, 
                          editable=False, default = uuid.uuid4)
    essay = models.OneToOneField(Essay, on_delete=models.CASCADE, related_name="feedback")
    spelling_errors_count = models.IntegerField(null=True, blank=True)
    content_relevance= models.BooleanField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class SpellingError(models.Model):
    id = models.UUIDField(primary_key=True, 
                          editable=False, unique=True, default=uuid.uuid4)
    word = models.TextField(null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    feedback = models.ForeignKey(Feedback, models.CASCADE, related_name="spelling_errors")