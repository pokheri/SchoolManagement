from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class IndexPageView(LoginRequiredMixin,TemplateView):
  template_name = 'dashboard/student/index.html'

class Base(TemplateView):
  template_name = 'dashboard/student/student_base.html'

class ProgressTemplateView(TemplateView):
  template_name = 'dashboard/student/progress.html'




