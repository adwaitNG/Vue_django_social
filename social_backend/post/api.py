from django.http import JsonResponse
from django.db.models import Q
from .forms import PostForm, AttachmentForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from account.models import User, FriendshipRequest
from account.serializer import UserSerializer
from .models import Post, Like, Comment, Trends
from .serializers import PostSerializer, PostDeatilSeraliser, CommentSerializer, TrendsSerialiser
from notification.utils import create_notification

@api_view(['GET'])
def post_list(request):

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(is_private=False).filter(created_by__in = list(user_ids)) 

    trend =request.GET.get('trend','')

    # print(trend)

    if trend:
        posts = posts.filter(is_private=False).filter(body__icontains=trend)
    print(posts)
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    if request.user.id == user.id:
        posts = Post.objects.filter(created_by_id = id)
    else :
        posts = Post.objects.filter(is_private=False).filter(created_by_id = id)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friend_req = True

    if request.user in user.friends.all():
        can_send_friend_req = False

    c1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    c2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if (c1 or c2):
        can_send_friend_req = False

    return JsonResponse( {'posts':post_serializer.data,
                          'user':user_serializer.data,
                          'can_send_friend_req':can_send_friend_req} , safe= False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        request.user.post_count = request.user.post_count +1
        request.user.save()
        serialiser = PostSerializer (post)
        
        return JsonResponse(serialiser.data, safe=False)
    else:
        return JsonResponse({'Error': "Some error during posting"})                    

@api_view(['POST'])
def post_like_request(request, id):

    post = Post.objects.get(id=id)

    if not post.likes.filter(created_by=request.user):

        like = Like.objects.create(created_by= request.user)

        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request=request, type_of_notification='postLike', post_id= post.id)

        return JsonResponse({"message": "Like created!!"})
    else:
        return JsonResponse({"message":"The post was already liked!"})    

@api_view(['GET'])
def post_details(request, id):

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter( Q(created_by__in = list(user_ids)) | Q(is_private=False)).get(id=id)

    return JsonResponse({'post': PostDeatilSeraliser(post).data})


@api_view(['POST'])
def post_create_comment_request(request, id):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    
    post = Post.objects.get(id = id)
    post.comments.add(comment)
    post.comments_count = post.comments_count +1
    post.save()

    notification = create_notification(request=request, type_of_notification='postComment', post_id= post.id)
    
    serialiser = CommentSerializer(comment)
    return JsonResponse(serialiser.data, safe=False)

@api_view(['GET'])
def get_Trends(request):
    trends = Trends.objects.all()
    serialiser = TrendsSerialiser(trends ,many=True)
    return JsonResponse(serialiser.data, safe=False)