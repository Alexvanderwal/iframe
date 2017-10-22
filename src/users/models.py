from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    avatar = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return str(self.user.username)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, settings.AUTH_USER_MODEL)