from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializer import UserSerializer
from post.models import Post
from post.serializers import PostSerializer

@api_view(['POST'])
def search(request):
    data = request.data

  
    query = data['query']
    # print(query)

    users = User.objects.filter(name__icontains=query)
    user_seralizer = UserSerializer(users, many=True)

    posts = Post.objects.filter(is_private=False).filter(body__icontains=query)
    post_seralizer = PostSerializer(posts, many=True)

    return JsonResponse({"users": user_seralizer.data,
                         "posts": post_seralizer.data}, safe=False)