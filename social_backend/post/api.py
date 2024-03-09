from django.http import JsonResponse
from .forms import PostForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from account.models import User
from account.serializer import UserSerializer
from .models import Post, Like
from .serializers import PostSerializer

@api_view(['GET'])
def post_list(request):

    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by__in = list(user_ids)) 

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id = id)

    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse( {'posts':post_serializer.data,
                          'user':user_serializer.data} , safe= False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

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
        return JsonResponse({"message": "Like created!!"})
    else:
        return JsonResponse({"message":"The post was already liked!"})    
