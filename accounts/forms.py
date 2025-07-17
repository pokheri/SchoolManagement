

from django import forms
from django.contrib.auth.models import User 
from .models import (
    Profile,


)

# user login form 



class UserLoginForm(forms.Form):

    username = forms.CharField(max_length=60 ,help_text="Enter your username Or email  ")
    password  = forms.CharField(max_length=20, widget=forms.PasswordInput())



    
class CreateUserForm(forms.ModelForm):

    password = forms.CharField(
        max_length=20, 
        widget=forms.PasswordInput(attrs={'placeholder': "Enter password"})
    )
    password2 = forms.CharField(
        max_length=20, 
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm password"})
    )

    class Meta:
        model = User  
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data



class PasswordChangeForm(forms.Form):

    username  = forms.CharField(max_length=50,  help_text="Your username or email ")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Current password ")
    new_password = forms.CharField(widget=forms.PasswordInput(), help_text="New  password ")


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
     

        if password and len(password)<12:
            self.add_error('new_password', "Your password is less secure make sure you create a strong password more than 12 character ")
        return cleaned_data


from django import forms

class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


