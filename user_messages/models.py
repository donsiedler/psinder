from django.db import models

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Thread(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

