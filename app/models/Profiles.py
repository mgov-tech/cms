from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    is_creator = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)

    class Meta:
        app_label = 'app'
        verbose_name = 'Usuários & Perfis'
        verbose_name_plural = 'Usuários & Perfis'

    def __str__(self):
        return self.username
