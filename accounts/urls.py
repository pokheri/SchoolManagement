

from django.urls import path
from . import views 
# app_name = 'accounts'
# urlpatterns  = [

#     path('login/', views.UserloginView.as_view(), name='login'), 
#     path('logout/', views.UserLogoutView.as_view(),name='logout'), 
#     path('create-account/', views.CreateNewUserView.as_view(),name='create_account'), 
#     path('change-password/', views.PasswordChangeView.as_view(),name='password_change'), 
#     path('reset-password/', views.PasswordResetView.as_view(), name='password-reset'),
#     path('reset-password-email/', views.PasswordResetEmailView.as_view(), name='password_reset_email'),
#     path('reset-password/<int:uid>/', views.ResetPasswordView.as_view(), name='reset_password'),
#     path('profile/', views.ProfileView.as_view(), name='profile'),



# ]


urlpatterns = [
    
    path('create-user/', views.CreateNewUser.as_view(), name='create_new_user'),
    path('login/', views.UserloginView.as_view(), name='login'), 
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(),name='change_password') , 
    path('reset-password/', views.PasswordResetView.as_view(), name='password-reset'),
    path('reset-password-email/', views.PasswordResetEmailView.as_view(), name='password_reset_email'),
    path('reset-password/<int:uid>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('profile/<str:flag>/<str:user_id>/', views.ProfileView.as_view(), name='profile'), 
    path('update-profile/<str:user_id>/', views.UpdateProfileView.as_view(), name='update_profile'), 
    path('delete-user/<str:pk>/', views.DeleteUserView.as_view(),name='delete_user'), 







]