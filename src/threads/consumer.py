from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.views.generic.edit import FormMixin
from django.forms.models import model_to_dict
from datetime import datetime
from .models import Post, Thread

class ThreadConsumer(FormMixin, WebsocketConsumer):
    def connect(self):
        # TODO: room vs roomgroup?
        self.room_name = self.scope['url_route']['kwargs']['thread_title']
        self.room_group_name = 'chat_{0}'.format(self.room_name)
        # Join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass
    import json
    # Receive message from webSocket
    def receive(self, text_data):
        print("text data", )
        text_data = json.loads(text_data)

        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'new_post',
                'content': text_data['content'],
                'thread_id': text_data['id'],
            }
        )

    # Receive message from the room group
    def new_post(self, event):
        print(self.scope['user'].profile.__dict__)
        user = self.scope['user']
        # print(dict(self.scope['user'].profile.avatar))
        content = event['content']
        thread_id = event['thread_id']
        thread = Thread.objects.get(pk=thread_id)
        print(thread)
        post = Post.objects.create(content=content, user=user, thread=thread) 
        post.save()
        user = {
            "avatar": "/media/" + str(self.scope['user'].profile.avatar),
            "description": str(self.scope['user'].profile.description),
            "time": str(datetime.now().today()),
            "username": self.scope['user'].username,
            "slug": str(self.scope['user'].profile.slug)
         }
        # print(json.dumps(model_to_dict()))
        print(content)
        self.send(text_data=json.dumps({
            'message': content,
            'user': user,
            'post_id': post.pk
        }))
        # send to socket

