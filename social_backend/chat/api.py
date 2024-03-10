from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from account.models import User
from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer ,ConversationMessageSerializer , ConverstionDetailSerializer


@api_view(['GET'])
def conversation_list(request):
    conversation = Conversation.objects.filter(users__in=list([request.user]))
    

    serializer = ConversationSerializer(conversation, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def converstation_details(request, id):

    conversation = Conversation.objects.filter(users__in=list([request.user])).get(id = id)
    serializer = ConverstionDetailSerializer(conversation)

    return JsonResponse( serializer.data, safe=False)



@api_view(['POST'])
def conversation_send_message(request, id):

    conversation = Conversation.objects.filter(users__in=list([request.user])).get(id = id)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conv_message = ConversationMessage.objects.create(
        conversation = conversation, 
        body = request.data.get('body'),
        sent_to = sent_to,
        created_by = request.user,
    )

    seralizer = ConversationMessageSerializer(conv_message)

    return JsonResponse(seralizer.data, safe=False)

@api_view(['GET'])
def conv_get_or_create(request, id):

    user = User.objects.get(id=id)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
        print(conversation)
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    seralizer = ConverstionDetailSerializer(conversation)


    return JsonResponse(seralizer.data, safe=False)

