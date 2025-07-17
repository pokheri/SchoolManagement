# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from django.contrib import messages
# from django.contrib.auth import login, logout , authenticate
# from django.views import generic
# from django.views import View
# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives, send_mail
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django import forms 
# from .signals import (
#     password_reset, 
#     password_changed
# )

# from django.forms import formset_factory, inlineformset_factory, modelformset_factory


# from .models import (
#     Profile,

# )


# from .forms import (
#     UserLoginForm, CreateUserForm, PasswordChangeForm, PasswordResetForm, 
#     ProfileForm
# )

# class  UserloginView(View):
#     redirect_field_name = 'next'


#     form = UserLoginForm()
#     def get(self, request, *args, **kwargs):
#         next_url = request.GET.get(self.redirect_field_name, "")
        
#         context = {
#             'form': self.form, 
#              "next": next_url,  
#         }
#         return render(request, 'accounts/login.html', context )
    
#     def post(self, request, *args, **kwargs):

#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             username = cd['username']
#             password = cd['password']
#             next_url = (
#             request.POST.get(self.redirect_field_name)
#             or request.GET.get(self.redirect_field_name)
#             )
            

#             user = authenticate(request,username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 if next_url:
#                     return redirect(next_url)
#                 return redirect('dash:index')
                
#         else:
#             messages.error(request, "Please enter the correct credentials ")

#         return render(request, 'accounts/login.html', {"form": form})
        


# class UserLogoutView(LoginRequiredMixin,View):

#     def get(self, request, *args, **kwargs ):

#         return render(request, 'accounts/logout_confirm.html')
    

#     def post(self, request, *args, **kwargs):

#         logout(request)
#         return redirect('dash:index')
    



# class CreateNewUserView(View):

#     def get(self,request, *args, **kwargs):

#         form = CreateUserForm()
#         context = {
#             'form': form,

#         }
#         return render(request, 'accounts/create_account.html', context )
    
#     def post(self, request, *args, **kwargs):

#         form = CreateUserForm(request.POST)
#         if form.is_valid():

#             cd  = form.cleaned_data
#             password = cd['password']
#             username = cd['username']
#             email = cd['email']

#             try:
#                 user  = User.objects.create_user(username=username, email=email, password=password)
#             except Exception as e :
#                 print(e)
#                 print('the fucking problem in  the create user ')
#             login(request, user)
#             return redirect('accounts:profile')
        
#         else: 
#             messages.error(request, "Please enter the right credentails ")
            
#         return render(request, 'accounts/create_account.html', {"form": form})
    
# class PasswordChangeView(View):
    
#     def get(self, request, *args, **kwargs):
#         form = PasswordChangeForm()

#         return render(request, 'accounts/password_change.html', {"form": form})
    
#     def post(self, request, *args, **kwargs):

#         form = PasswordChangeForm(request.POST)

#         if form.is_valid():

#             cd = form.cleaned_data
#             username = cd['username']
#             password = cd['password']
#             new_password = cd['new_password']

#             user = authenticate(request,username=username, password=password)
#             if user is not None:
                
#                 user.set_password(new_password)
#                 user.save()
#                 password_changed.send(sender=user)
#                 login(request,user)
#                 messages.success(request, 'Password change successfuly ')
#                 return redirect('dash:index')
#             else:
#                 # if the user is none 
#                 messages.error(request, "Please enter the right credentials ")
        
#         return render(request, 'accounts/password_change.html', {"form": form})
    
            



# class PasswordResetView(generic.TemplateView):
#     template_name = 'accounts/reset.html'
    

# class PasswordResetEmailView(View):

#     def post(self, request):
#         email = request.POST.get("email")
#         user = User.objects.filter(email=email).first()

#         if user:
#             reset_link = request.build_absolute_uri(
#                 reverse('accounts:reset_password', kwargs={'uid': user.id})
#             )

#             subject = "Reset Your Password"
#             from_email = "admin@yourdomain.com"
#             to_email = [user.email]

#             context = {
#                 'username': user.username,
#                 'reset_link': reset_link
#             }

#             html_content = render_to_string('accounts/password_reset_email.html', context)
#             text_content = f"Hi {user.username}, click the link to reset your password: {reset_link}"

#             email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
#             email_message.attach_alternative(html_content, "text/html")
#             email_message.send()

#         return render(request, 'accounts/email_confirmation.html')
    


# class ResetPasswordView(View):

#     def get(self, request, uid):
#         form = PasswordResetForm()
#         return render(request, 'accounts/reset_password_form.html', {'form': form})

#     def post(self, request, uid):
#         user = get_object_or_404(User, pk=uid)
#         form = PasswordResetForm(request.POST)

#         if form.is_valid():
#             password = form.cleaned_data.get('password')
#             user.set_password(password)
#             user.save()
#             password_reset.send(sender=user)
#             messages.success(request, 'Password reset successful.')
#             return redirect('accounts:login')

#         messages.error(request, 'Please correct the errors below.')
#         return render(request, 'accounts/reset_password_form.html', {'form': form})



# class ProfileView(LoginRequiredMixin,View):


#     def get(self, request, *args, **kwargs):
        
#         user = request.user 
#         if hasattr(user,'profile'):
#             context = {
#                 'profile': user.profile
#             }
#             return render(request,'profile/profile.html', context  )
        
        
#         context = {
#             'form': ProfileForm(), 
            
            
#         }
#         return render(request, 'profile/create_profile.html', context )
    
#     def post(self, request, *args, **kwargs):

#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             profile = form.save(commit=False)
#             profile.user = request.user 
#             profile.save()

#             # returning the user somewhere like index 
#             return redirect('dash:index')
        
#         context = {
#             'form': form 
#         }
#         return render(request, 'profile/create_profile.html', context )

