from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True)
    active = models.BooleanField(default=True)
    latest_thread = models.ForeignKey('threads.Thread', null=True, blank=True, related_name='latest_thread')
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def thread_count(self):
        return self.thread_set.all().count()

    def thread_total_post_count(self):
        threads = self.thread_set.all()
        count = 0
        for thread in threads:
            count += thread.post_count
        return str(count)