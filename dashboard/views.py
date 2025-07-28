from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model 


def index(request):
  return render(request, 'dashboard/student/index.html')