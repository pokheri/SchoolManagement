from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model 


def index(request):
    
    print(get_user_model())
    return HttpResponse(get_user_model())


# Create your views here.
