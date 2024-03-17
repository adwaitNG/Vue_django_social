from django.shortcuts import render
from django.http import HttpResponse
from .models import User
# Create your views here.

def activateEmail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id','')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()

        return HttpResponse("The user is activated, continue to the login Page :http://localhost:5173/login")

    return HttpResponse("The url is not Valid")

    