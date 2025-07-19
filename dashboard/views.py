from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model 


def index(request):
    
    print(get_user_model())
    return HttpResponse(f'hey my name is dinesh singh how are you doing man {request.user.username}')


# Create your views here.
