from rest_framework import serializers

from account.serializer import UserSerializer
from .models import Post, Comment, Trends, PostAttachment


## 'created_by_formatted' is actually 'created_at_formatted' gives the time of data , need to change to that 

class PostAttachmentSerializer (serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image', )

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only = True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_by_formatted','likes_count','comments_count', 'attachments',)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    # attachments = PostAttachmentSerializer(read_only = True, many=True)

    class Meta:
        model = Comment
        fields = ('id','body', 'created_by_formatted', 'created_by', )

class PostDeatilSeraliser(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many = True)
    attachments = PostAttachmentSerializer(read_only = True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_by_formatted','comments_count','likes_count', 'comments', 'attachments')


class TrendsSerialiser(serializers.ModelSerializer):

    class Meta:
        model= Trends
        fields= ('id', 'hashtag', 'occurences', )