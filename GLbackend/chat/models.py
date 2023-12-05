import uuid
from django.db import models
from django.utils.timesince import timesince
from account.models import User

# model for the conversation/message
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations') #reference to the users who are connected to the conversation
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add - updated when added to database
    modified_at = models.DateTimeField(auto_now=True) #auto_now - everytime it is saved, automatically updates

    def modified_at_formatted(self):
        return timesince(self.created_at)

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE) #if a conversation is deleted, all messages will also be deleted
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE) #if receiver (user) is deleted, messages are also deleted
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE) #if user is deleted, messages are also deleted 

    def created_at_formatted(self):
        return timesince(self.created_at)