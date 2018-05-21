from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from django.views.generic.edit import FormMixin
from django.forms.models import model_to_dict


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

    # Receive message from webSocket
    def receive(self, text_data):
        print(text_data)

        # Send the message to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'new_post',
                'content': text_data
            }
        )

    # Receive message from the room group
    def new_post(self, event):
        print(self.scope['user'].profile.__dict__)
        user = {"description": self.scope['user'].profile.description,
                "username": self.scope['user'].username}
        # print(json.dumps(model_to_dict()))
        content = event['content']
        self.send(text_data=json.dumps({
            'message': content,
            'user': user
        }))
        # send to socket

