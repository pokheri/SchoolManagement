from django.db import models


# Create your models here.
from django.forms.formsets import formset_factory


from django.contrib.auth.models import AbstractUser
from django.conf import settings

User = settings.AUTH_USER_MODEL 

class CustomUser(AbstractUser):

    class UserRole(models.TextChoices):
        STU = 'ST', 'Student'
        T = 'T', 'Teacher'

    role = models.CharField(max_length=3, choices=UserRole, default=UserRole.STU)

class AbstractProfile(models.Model):
    """
     shared information of all users are here 
    """
    class Gender(models.TextChoices):
        M = 'M', "Male"
        F = 'F', 'Female'

   
    gender = models.TextField(max_length=1, choices=Gender,default=Gender.M)
    age = models.PositiveSmallIntegerField()
    father_name  = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users/images/', null=True, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=6)
    state = models.CharField(max_length=50)
    address = models.TextField(max_length=100)
    
    class Meta:
        abstract=True


class StudentProfile(AbstractProfile):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    # classname
    #courses 
    # other information 
    def __str__(self):
        return f'Student {self.user.first_name}'
    

class  TeacherProfile(AbstractProfile):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    id  = models.BigAutoField(primary_key=True, unique=True)
    maried = models.BooleanField(default=False)
    salary= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Teacher {self.user.first_name}'
    
    







# class Profile(models.Model):

#     class UserRole(models.TextChoices):

#         CI = 'CI', 'Citizens'
#         OF = 'OF', 'Officer'
#         MA = 'MA','Manager'
#         A ='A','Admin'


#     class GenderChoice(models.TextChoices):
#         M = 'M',"Male"
#         F = 'F', "Female"
        
    
    
#     id = models.PositiveIntegerField(primary_key=True, verbose_name='your adhar number ', unique=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     name = models.CharField(max_length=50)
#     age = models.PositiveSmallIntegerField()
#     gender = models.CharField(max_length=2, choices=GenderChoice)
#     phone = models.CharField(max_length=12)
#     user_role = models.CharField(max_length=2, choices=UserRole, default=UserRole.CI)
#     picture = models.ImageField(upload_to='resident/images',null=True,blank=True)
#     zip_code  = models.CharField(max_length=12)
#     created_at = models.DateTimeField(auto_now_add=True)
#     update_at= models.DateTimeField(auto_now=True)



#     def __str__(self):
#         return f'profile {self.name}'
    



 

    






