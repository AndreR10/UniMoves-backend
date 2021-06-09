from django.db import models

from datetime import datetime


class Message(models.Model):
    chat = models.ForeignKey("chat.Chat", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    date = models.DateTimeField(default=datetime.now)
    # viewed = models.BooleanField(default=False)
