from django.db import models
from django.contrib.auth.models import User
from helpers.models import trackingModel
from django.conf import settings


class Todo(trackingModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
