from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SingupForm, ProfileForm
from .models import User, FriendshipRequest
from .serializer import UserSerializer, FriendshipRequestSerializer

from notification.utils import create_notification
@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar':request.user.get_avatar(),
    }, safe=False)


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
        user = form.save()
        user.is_active = False
        user.save()
        url = f'http://127.0.0.1:8000/api/activate-account/?email={user.email}&id={user.id}'
        
        message="success"
        send_mail(
            "Verify the account",
            f"The url for activating your account is : {url}",
            "noreply@gmail.com",
            [user.email],
            fail_silently=False
        )

    else:
        message= form.errors.as_json()
        

    
    return JsonResponse({'message':message}, safe=False)



@api_view(['POST'])
def send_friend_request(request, id):
    # print("firendship", id)
    user = User.objects.get(id=id)
    # print(user.name)
    # print(request.user.name)
    c1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    c2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    

    if (not c1 and not c2):
        friendshipRequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        notification = create_notification(request=request, type_of_notification='newFriendRequest', friend_request_id= friendshipRequest.id)
        return JsonResponse({"kmessage":FriendshipRequestSerializer(friendshipRequest).data})
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

    notification = create_notification(request=request, type_of_notification='acceptedFriendRequest', friend_request_id= friendship_Request.id)

    return JsonResponse({"message":"Friendship Request Updated"})


@api_view(['POST'])
def editProfile(request):
    user = request.user
    email = request.data.get('email')
    if (User.objects.exclude(id=user.id).filter(email = email).exists()):
        return JsonResponse({"message":"Email already exitst!"})

    form = ProfileForm(request.POST, request.FILES, instance=user)


    # print(request.FILES)

    
    if form.is_valid():
        form.save()
        
    serializer = UserSerializer(user)

    # user.name = request.data.get('name')
    # user.email = email
    # user.save()

    return JsonResponse({"message":"success", 'user':serializer.data})


@api_view(['POST'])
def editPassword(request):
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)
    print(request.data)
    if form.is_valid():
        form.save()

        return JsonResponse({"message":"success"}) 
    
    else:
        return JsonResponse({'message':form.errors.as_json()}, safe=False)
        
@api_view(['GET'])
def friends_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many= True)
    
    return JsonResponse(serializer.data, safe=False)
     
