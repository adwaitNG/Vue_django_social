from django.db import models
from django.utils import timesince
import uuid
from account.models import User
from post.models import Post


class Notifications (models.Model):
    NEWFRIENDREQUEST = 'newFriendRequest' 
    ACCEPTEDFRIENDREQUEST = 'acceptedFriendRequest' 
    REJECTEDFRIENDREQUEST = 'rejectedFriendRequest'
    POST_LIKE = 'postLike'
    POST_COMMENT = 'postComment'

    CHOICE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friendrequest'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
        (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment')
    )

    id =  models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read= models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length = 50, choices = CHOICE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank =True, null = True)
    created_by = models.ForeignKey(User, related_name='created_notification', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name= 'recived_notification', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def created_by_formatted(self):
        return timesince(self.created_at)
