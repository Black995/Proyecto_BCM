from asyncio.windows_events import NULL
from django.db import models
from users.models import User
from configuration.models import ProductActivation
from datetime import datetime, timedelta, tzinfo
import urllib3


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

    @classmethod
    def RemainingActivationTimeNotifiaction(cls):
        activation = ProductActivation.objects.all()
        exp_date = activation[0].activation_date + timedelta(weeks=26)
        http = urllib3.PoolManager()
        res = http.request('GET','http://just-the-time.appspot.com/')
        
        result = res.data

        date_str = result.decode('utf-8')

        dateL = date_str.split(" ")

        date = datetime.strptime(dateL[0], '%Y-%m-%d').date()
        title = "Tiempo para expiración de producto"
        description = ""
        notif =NULL
        if ((exp_date-date).days()==91):
            description = "Estimado usuario, le quedan 3 meses de activación del producto. Recuerde renovar la llave para poder seguir disfrutando del sistema."
            notif = Notification.objects.create(
                title=title, 
                description=description,
                type=1
            )

        if ((exp_date-date).days()==60):
            description = "Estimado usuario, le quedan 2 meses de activación del producto. Recuerde renovar la llave para poder seguir disfrutando del sistema."
            notif = Notification.objects.create(
                title=title, 
                description=description,
                type=1
            )

        if ((exp_date-date).days()==30):
            description = "Estimado usuario, le queda 1 mes de activación del producto. Recuerde renovar la llave para poder seguir disfrutando del sistema."
            notif = Notification.objects.create(
                title=title, 
                description=description,
                type=2
            )

        if ((exp_date-date).days()<=15):
            description = "Estimado usuario, le quedan menos de 2 semanas de activación del producto. Recuerde renovar la llave para poder seguir disfrutando del sistema."
            notif = Notification.objects.create(
                title=title, 
                description=description,
                type=3
            )

        admins = User.objects.filter(is_superuser=True)
        user_list = []
        email_list = []
        for a in admins:
            user_list.append(a)
            email_list.append(a.email)
            if (notif is not NULL):
                n_u = N_U.objects.create(read=False,user=a.id,notification=notif.id)
        if notif is not NULL:        
            """
            email_message = EmailMessage(
                subject=title,
                body=description,
                from_email=settings.EMAIL_HOST_USER,
                bcc=email_list
            )
            email_message.send()
            """
        




class N_U(models.Model):

    read = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, related_name='user_n_u',
                             on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, related_name='notification_n_u',
                              on_delete=models.CASCADE)
