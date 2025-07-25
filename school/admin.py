from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import ( 
    SchoolClass,
    Subject, 
    Assignment, 
    TeachingAssignment, 
    AssignmentSubmission,
    Examination, 
    ExamMarks,
    SubjectMarks
)


@register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):

    list_display = ['name','get_section_display', 'class_teacher__first_name','id']

@register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    
    list_display= ['name', 'code', 'id']

@register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = ['title', 'teacher__first_name', 'class_name__name', 'subj__name', 'id']

@register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):

    list_display = ['teacher__first_name', 'class_name__name','id']


admin.site.register(AssignmentSubmission)
admin.site.register(Examination)
admin.site.register(SubjectMarks)
admin.site.register(ExamMarks)
