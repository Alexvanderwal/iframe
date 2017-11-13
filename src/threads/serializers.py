from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # date_created = models.DateTimeField(auto_now_add=True)
    # date_modified = models.DateTimeField(auto_now=True)
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', null=True, blank=True)
    # content = FroalaField()
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    # thread = models.ForeignKey('threads.Thread', null=True, blank=True)
    class Meta:
        model = Post
        fields = ('content',)