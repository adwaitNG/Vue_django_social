from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SingupForm
from .models import User, FriendshipRequest
from .serializer import UserSerializer, FriendshipRequestSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data

    message = 'success'

    form = SingupForm({
        'email':data.get('email'),
        'name':data.get('name'),
        'password1':data.get('password1'),
        'password2':data.get('password2'),
    })

    if form.is_valid():
        form.save()
        #Verification Email

    else:
        message= 'error'

    context = {'message':message}
    
    return JsonResponse(context)



@api_view(['POST'])
def send_friend_request(request, id):
    # print("firendship", id)
    user = User.objects.get(id=id)
    print(user.name)
    print(request.user.name)
    c1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    c2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if (not c1 and not c2):
        friendshipRequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        return JsonResponse({"message":FriendshipRequestSerializer(friendshipRequest).data})
    else:
        return JsonResponse({"message" : "Request already sent"})
    

@api_view(['GET'])
def friends( request, id):
    user = User.objects.get(id=id)
    requests = []


    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for = request.user, status =FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True).data

    friends = user.friends.all()

    return JsonResponse({"requests": requests,
                         "friends": UserSerializer(friends, many=True).data,
                         "user": UserSerializer(user).data
                         }, safe=False)

@api_view(['POST'])
def handel_friend_request(request, id, status):
    user = User.objects.get(id=id)
    
    friendship_Request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_Request.status = status
    friendship_Request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count +1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count+1
    request_user.save()

    return JsonResponse({"message":"Friendship Request Updated"})