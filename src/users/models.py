import datetime
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.conf import settings

import os

from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    slug = models.SlugField(blank=True, editable=True)
    description = models.CharField(
        _('Description'), max_length=150, help_text=_('Add a sassy description for your profile'), blank=True)
    avatar = models.ImageField(
        upload_to='display_pictures', max_length=500, blank=True)

    def __str__(self):
        return str(self.user.username)

    @property
    def role(self):
        if self.user.is_staff:
            return "Staff"

    @property
    def post_count(self):
        return self.user.posts.all().count()

    @property
    def thread_count(self):
        return self.user.threads.all().count()

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    @property
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def online_status(self):
        if self.online:
            return "Online"
        else:
            return "Offline"

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


def pre_save_user_model_receiver(sender, instance, *args, **kwargs):
    if (not instance.slug and instance.user.username) or (slugify(instance.user.username) != instance.slug):
        print('test')
        instance.slug = slugify(instance.user.username)
        instance.save()





pre_save.connect(pre_save_user_model_receiver, Profile)
post_save.connect(post_save_user_model_receiver, settings.AUTH_USER_MODEL)