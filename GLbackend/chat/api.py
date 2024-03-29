
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer
from rest_framework.response import Response
import pusher


pusher_client = pusher.Pusher(
  app_id='1725847',
  key='122926f4663427b23929',
  secret='fcac78ecc03cb83bc6a3',
  cluster='ap1',
  ssl=True
)

@api_view(['GET'])
def conversation_list(request):
    #conversations where you are part of the user's list
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)
    
    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))
    
    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()
    
    serializer = ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    
    for user in conversation.users.all():
        if user != request.user:
            sent_to = user
    
    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
    )
    
    serializer = ConversationMessageSerializer(conversation_message)
    
    pusher_client.trigger(f'conversation_{pk}', 'new_message', serializer.data)
    
    return JsonResponse(serializer.data, safe=False)




