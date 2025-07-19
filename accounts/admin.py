from django.contrib import admin

from .models import(
    CustomUser, 
    StudentProfile, 
    TeacherProfile 
)


class StudentProfileAdmin(admin.ModelAdmin):

    list_display = ['user__username', 'id']


class TeacherProfileAdmin(admin.ModelAdmin):
        
    list_display = ['user__username', 'id']


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ['username', 'id']



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)


