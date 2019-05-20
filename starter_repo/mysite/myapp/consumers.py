# myapp/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # The ChatInstance is a self variable because I want it to be part of
        # the class's data members, because it will be accessed in other
        # functions.
        #
        # If we are the first user to join the chat room, we create a new ChatInstance,
        # otherwise we just connect to that already existing ChatInstance.
        #
        # If that chat room already existed, then self.new_chat_instance will
        # automatically be set to the correct chat room model.
        # If that chat room did not exist previously, then we create it.
        self.new_chat_instance = None
        try:
            self.new_chat_instance = models.ChatInstance.objects.get(chat_name=self.room_name)
        except models.ChatInstance.DoesNotExist:
            # Create a new ChatInstance and save it into the database.
            self.new_chat_instance = models.ChatInstance()
            self.new_chat_instance.chat_name = self.room_name
            # new_chat_post.chat_date is automatically set
            self.new_chat_instance.save()  # store it into the database

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        pipe_delimiter = message.find('|')
        # Get all characters from the beginning of the string to pipe_delimiter - 1.
        message_header = message[:pipe_delimiter]
        # Get substring starting at the character immediately after the pipe_delimiter,
        # all the way until the end.
        message_body = message[pipe_delimiter + 1:]

        # We save every chat post/message that we recieve into the database.
        new_chat_post = models.ChatPost()
        new_chat_post.author_name = message_header
        # new_chat_post.chat_date is automatically set
        new_chat_post.chat_content = message_body
        new_chat_post.chat_instance = self.new_chat_instance
        new_chat_post.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))