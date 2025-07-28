from django.urls import path
from . import views 

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'), 
    path('base/', views.Base.as_view()), 
    path('progress/', views.ProgressTemplateView.as_view(), name='progress'), 
    


]