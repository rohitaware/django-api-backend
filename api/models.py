from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    date = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message from {self.user.username} on {self.date}"

        