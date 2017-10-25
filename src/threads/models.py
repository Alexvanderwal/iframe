from django.db import models, transaction, IntegrityError
from django.conf import settings
# Create your models here.
from django.db.models.signals import post_save
from django.utils import timezone
from froala_editor.fields import FroalaField

from .choices import PinStatus


class Thread(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    starter = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=False, null=True)
    initial_post = models.OneToOneField('threads.Post', related_name='initial_post', null=True)
    pin_status = models.CharField(
        max_length=50, choices=PinStatus.choices, default=PinStatus.none)
    last_post = models.ForeignKey('threads.Post', null=True, blank=True, related_name='last_post')

    @property
    def post_count(self):
        return self.post_set.all().exclude(id=self.initial_post_id).count()

    @property
    def get_last_post(self):
        return self.last_post or self.initial_post

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'category')

@transaction.atomic
def post_save_thread_model_receiver(sender, instance, created, *args, **kwargs):
    try:
        with transaction.atomic():
            if created:
                initial_post = instance.initial_post
                initial_post.thread = instance

                initial_post.save()
            category = instance.category
            category.latest_thread = instance
            category.save()
    except IntegrityError:
        pass


post_save.connect(post_save_thread_model_receiver, Thread)


class Post(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', null=True, blank=True)
    content = FroalaField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    thread = models.ForeignKey('threads.Thread',  null=True, blank=True)

    def update_thread_update_date(self):
        self.thread.date_updated = timezone.now()
        self.thread.save()

    def update_last_post(self, post):
        self.thread.last_post = post
        self.thread.save()

    def get_date(self):
        return self.date_modified if self.date_modified > self.date_created else self.date_created

    def __str__(self):
        return str('{0} on {1}'.format(self.user.username, self.thread))


@transaction.atomic
def post_save_post_model_receiver(sender, instance, created, *args, **kwargs):
    """
    Function is atomic to ensure last_post is always the last post posted in the thread.
    """
    try:
        with transaction.atomic():
            if instance.thread:
                if created:
                    instance.update_last_post(instance)
                instance.update_thread_update_date()
    except IntegrityError:
        # TODO Fixme
        pass




post_save.connect(post_save_post_model_receiver, Post)
