from django.db import models
from users.models import User


class Notification(models.Model):
    title = models.TextField()
    description = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User)

