from django import forms
from django.conf import settings
from django.contrib.auth import(
    get_user_model, 
  
) 
from .models import (
    StudentProfile, 
    TeacherProfile 
)

User = get_user_model()

class UserCreateForm(forms.ModelForm):
    password =  forms.CharField(widget=forms.PasswordInput(),max_length=20)
    password_2  = forms.CharField(widget=forms.PasswordInput(), max_length=20)
    
    class Meta: 
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'role']

    def clean(self):
        data = super().clean()
        ps = data['password']
        ps2 = data['password_2']
        if ps and ps2 and ps !=ps2 :
            self.add_error('password', 'The password do not match ')
        return data 
    
class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=20)


class PasswordChangeForm(forms.Form):

    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=20, widget=forms.PasswordInput())


    def clean(self):
        data =  super().clean()
        pas  = data.get('password')
        pass2 = data.get('new_password')

        if pas and pass2 and pas==pass2:
            self.add_error('pass2', 'Please add new password ')
        return data  

class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = '__all__'
        exclude = ['user']
    
class TeacherProfileForm(forms.ModelForm):

    class Meta: 
        model = TeacherProfile
        fields = '__all__'
        exclude = ['employee_id', 'user']

    