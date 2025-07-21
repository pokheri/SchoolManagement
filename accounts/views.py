from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django import forms
from django.conf import settings
from guardian.mixins  import PermissionRequiredMixin as guardian_permissions 
from django.contrib.auth import (
    get_user_model, 
    authenticate, 
    login, 
    logout
)
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.views import View
from .forms import (
    UserCreateForm,
    UserLoginForm, 
    PasswordChangeForm, 
    PasswordResetForm, 
    StudentProfileForm, 
    TeacherProfileForm
)
from .models import (
    StudentProfile, 
    TeacherProfile
)
from .signals import(
    my_profile_permission_signal
)

User = get_user_model()


class CustomException(Exception):
    """ The custom Exception class """
    pass 

class CreateNewUser(LoginRequiredMixin, PermissionRequiredMixin, View):
    
    permission_required = 'accounts.add_customuser'
    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        context = {
            'form': form 
        }
        return render(request, 'accounts/create_account.html', context )

    def post(self, request, *args, **kwargs):

        form = UserCreateForm(request.POST)
        if form.is_valid(): 
            data = form.cleaned_data
            user = form.save(commit=False) 
            password = data.get('password')
            user.set_password(password)
            user.save() 
            # based on the user role(student, teacher or staff ) we will redirect to the profile page 
            flag = 1 if  user.role=='ST' else 0 
            return redirect('profile', user_id=user.id)
            
            
        else:
            messages.error(request, 'We are getting some problem with user registration please enter the correct info. ')
        return  render(request, 'accounts/create_account.html', {'form': form})
    
class  UserloginView(View):

    redirect_field_name = 'next'
    form = UserLoginForm()
    def get(self, request, *args, **kwargs):
        next_url = request.GET.get(self.redirect_field_name, "")
        
        context = {
            'form': self.form, 
             "next": next_url,  
        }
        return render(request, 'accounts/login.html', context )
    
    def post(self, request, *args, **kwargs):

        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            next_url = (
            request.POST.get(self.redirect_field_name)
            or request.GET.get(self.redirect_field_name)
            )
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                return redirect('index')
            else: 
                # if the credential are not correct 
                messages.error(request, 'Oh there is problem,  the credential are not matching ')
        else:
            messages.error(request, "Please enter the correct credentials ")

        return render(request, 'accounts/login.html', {"form": form})
        
class UserLogoutView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs ):

        return render(request, 'accounts/logout_confirm.html')
    
    def post(self, request, *args, **kwargs):

        logout(request)
        return redirect('index')
    
class PasswordChangeView(LoginRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm()

        return render(request, 'accounts/password_change.html', {"form": form})
    
    def post(self, request, *args, **kwargs):

        form = PasswordChangeForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            new_password = cd['new_password']

            user = authenticate(request,username=username, password=password)
            if user is not None:
                
                user.set_password(new_password)
                user.save()
                # password_changed.send(sender=user)
                login(request,user)
                messages.success(request, 'Password changed successfuly ')
                return redirect('index')
            else:
                # if the user is none 
                messages.error(request, "User with this  credentials  do not exists in ")
        
        return render(request, 'accounts/password_change.html', {"form": form})

class PasswordResetView(generic.TemplateView):

    template_name = 'accounts/reset.html'
    
class PasswordResetEmailView(View):

    def post(self, request):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'uid': user.id})
            )

            subject = "Reset Your Password"
            from_email = "admin@yourdomain.com"
            to_email = [user.email]

            context = {
                'username': user.username,
                'reset_link': reset_link
            }

            html_content = render_to_string('accounts/password_reset_email.html', context)
            text_content = f"Hi {user.username}, click the link to reset your password: {reset_link}"

            email_message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

        return render(request, 'accounts/email_confirmation.html')
  
class ResetPasswordView(View):

    def get(self, request, uid):
        form = PasswordResetForm()
        return render(request, 'accounts/reset_password_form.html', {'form': form})

    def post(self, request, uid):
        user = get_object_or_404(User, pk=uid)
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            # password_reset.send(sender=user)
            messages.success(request, 'Password reset successful.')
            return redirect('login')

        messages.error(request, 'Enter the correct and strong password .')
        return render(request, 'accounts/reset_password_form.html', {'form': form})

# by admin only 
class ProfileView(LoginRequiredMixin,View):

    def dispatch(self, request, *args, **kwargs):

        self.user_id = kwargs.get('user_id')
        self.target_user = get_object_or_404(User, pk= self.user_id)
        self.flag = self.target_user.role 
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_class(self):

        if self.flag =='ST':
            return  StudentProfileForm
        return TeacherProfileForm
    
    def get_custom_context(self, form=None):
        return {
            'flag': self.flag, 
            'user': self.user_id, 
            'form': self.get_form_class() if form is None else form 
        }
    
    def get(self, request, *args, **kwargs):
        
        context =self.get_custom_context()
        return render(request, 'profile/create_profile.html', context )
    
    def post(self, request, *args, **kwargs):
        if self.flag and self.target_user:
            form = self.get_form_class()
            form = form(request.POST)

            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = self.target_user
                profile.save() 
                # for external functionality of differ model, do it here 
                my_profile_permission_signal.send(sender=self.target_user, instance= profile) # signal 
                return redirect('index')
            else:
                messages.error(request, "The form data is invalid please try again ")
                context = self.get_custom_context(form)
                return render(request, 'profile/create_profile.html', context)
        else:
            raise CustomException('Hey we are in the profile view and the error hit here ')

class UpdateProfileView(LoginRequiredMixin, guardian_permissions, View):

    permission_required = 'accounts.my_profile'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):

        self.user_id = kwargs.get('user_id')
        self.target_user =get_object_or_404(User, pk=self.user_id)
        self.flag = self.target_user.role 
        self.profile = self.target_user.get_profile()
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        return self.target_user.get_profile()

    def get_form_class(self):
        if self.flag =='ST':
            return StudentProfileForm
        return TeacherProfileForm
    
    def get(self, request, *args, **kwargs ):

        form_class  =self.get_form_class()
        form = form_class(instance=self.profile)    
        context = {
            'form': form 
        }
        return render(request, 'profile/update_profile.html', context)
    
    def post(self, request, *args, **kwargs):

        form_class =  self.get_form_class()
        form = form_class(request.POST, instance = self.profile)
        if form.is_valid():
            form.save()
            return redirect('index')
        else: 
            messages.error(request, 'Enter the correct data ')
        return HttpResponse('what is going on man ')
    
class DeleteUserView(LoginRequiredMixin,PermissionRequiredMixin, generic.DeleteView):

    permission_required = ('accounts.admin_only')
    model = User
    template_name= 'accounts/delete_user.html'
    success_url  = reverse_lazy('index')






          


