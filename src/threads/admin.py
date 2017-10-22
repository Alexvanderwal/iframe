from django.contrib import admin
from .models import Post, Thread
# Register your models here.

admin.site.register(Thread)
admin.site.register(Post)