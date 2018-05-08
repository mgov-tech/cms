from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=160)

    class Meta:
        app_label = 'app'
        verbose_name = 'CLIENTES'
        verbose_name_plural = 'CLIENTES'

    def __str__(self):
        return self.name
