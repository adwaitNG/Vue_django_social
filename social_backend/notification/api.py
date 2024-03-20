from .serializers import NotificationSerializer
from .models import Notifications

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

@api_view(['GET'])
def notifications(request):
    #Using Related Name 
    recived_notification = request.user.recived_notification.filter(is_read=False)
    serializer = NotificationSerializer(recived_notification ,many=True)

    return JsonResponse(serializer.data , safe=False)

@api_view(['POST'])
def readNotificationRequest(request, id ):
    notification = Notifications.objects.filter(created_for = request.user).get(id = id)
    notification.is_read = True
    notification.save()

    return JsonResponse ({'message':"Notification Marked as Read"})
