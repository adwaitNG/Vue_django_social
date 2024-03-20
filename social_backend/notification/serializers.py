from rest_framework import serializers
from .models import Notifications
from post.serializers import PostAttachmentSerializer
from account.serializer import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    # created_by =  UserSerializer(read_only=True)
    post = PostAttachmentSerializer(read_only=True)
    class Meta:
        model = Notifications
        # fields = ('id', 'body', 'is_read', 'type_of_notification', 'created_by', 'created_by_formatted')
        fields = ('id', 'body', 'type_of_notification' ,'post', 'created_for')