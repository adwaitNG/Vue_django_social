from django.http import JsonResponse
from .forms import PostForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


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

    return JsonResponse({"BAkc": "Back"})