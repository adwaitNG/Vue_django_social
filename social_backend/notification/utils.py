from .models import Notifications
from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type_of_notification, post_id = None, friend_request_id = None):
    post = None
    if type_of_notification  == 'postLike':
        body = f'{request.user.name} liked one of your post!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification  == 'postComment':
        body = f'{request.user.name} commented on one of your post!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif type_of_notification  == 'newFriendRequest':
        body = f'{request.user.name} sent you a friend request'
        friend_request = FriendshipRequest.objects.get(pk = friend_request_id)
        created_for = friend_request.created_for

    elif type_of_notification  == 'acceptedFriendRequest':
        body = f'{request.user.name} accepted your friend request'
        friend_request = FriendshipRequest.objects.get(pk = friend_request_id)
        created_for = friend_request.created_for

    elif type_of_notification == 'rejectedFriendRequest':
        body = f'{request.user.name} rejected your friend request'
        friend_request = FriendshipRequest.objects.get(pk = friend_request_id)
        created_for = friend_request.created_for

    notification = Notifications.objects.create( 
        created_by = request.user,
        type_of_notification = type_of_notification,
        body = body,
        post=post,
        created_for = created_for,

        )
    return notification

