from django.db import models
from users.models import User


class Notification(models.Model):
    
    INFORMATION = 1
    WARNING = 2
    DANGER = 3
    TYPE = (
        (INFORMATION, 'Information'),
        (WARNING, 'Warning'),
        (DANGER, 'Danger'),
    )

    title = models.TextField()
    description = models.TextField()
    type = models.SmallIntegerField(choices=TYPE)
    date = models.DateTimeField(auto_now=True)
    # users = models.ManyToManyField(User, related_name='user_notifications')


class N_U(models.Model):

    read = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, related_name='user_n_u',
                             on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, related_name='notification_n_u',
                              on_delete=models.CASCADE)
