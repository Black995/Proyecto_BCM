from django.db import models


class Usuario(models.Model):

    correo = models.EmailField(unique=True)
    contrasenna = models.CharField(max_length=100)
