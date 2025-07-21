from django.db import models
from accounts.models import (
    StudentProfile, 
    TeacherProfile 
)
from django.conf import settings
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL



class TimeStamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True


class SchoolClass(TimeStamp):

    class SectionChoice(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'

    name = models.CharField(max_length=50)
    section  = models.CharField(max_length=1, choices=SectionChoice)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'T'}, related_name='my_class')
    class_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Stu'})
    subjects = models.ManyToManyField('Subject', related_name='class_room')
    location  = models.TextField()

    class Meta:
        unique_together = ['name', 'section']

    def __str__(self):
        return f'Class {self.name} - Section {self.section}'


class Subject(TimeStamp):

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
     return f'{self.code, self.name}'
    
class Assignment( TimeStamp):

    def assignment_upload_path(instance, filename):
        return f'assignments/class_{instance.class_name.name}/{filename}'

    title = models.CharField(max_length=50)
    teacher   = models.ForeignKey(User,on_delete=models.CASCADE, limit_choices_to={'role': 'T'})
    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subj = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    assignment_file = models.FileField(upload_to=assignment_upload_path)
    message = models.TextField(null=True, blank=True)
    last_date_sub  = models.DateTimeField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'teacher', 'class_name'],
                                    name='teacher_class_and_assignment_unique_together', 
                                    violation_error_message="you can't do this same teacher with the same title ")
        ]

    def __str__(self):
        return f'Assignment {self.subj.name}'
    

class TeachingAssignment(TimeStamp):

    teacher = models.ForeignKey(User, limit_choices_to={'role': 'T'}, on_delete=models.CASCADE)
    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='teachers')
    subjects    = models.ManyToManyField(Subject,related_name='subject_teachers')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'class_name'],
                                     name='teacher_and_class_are_unique_togethter',
                                     violation_error_message=' teacher and class name already assigned with all subjects that he/she gona teach to the class ' )
        ]
    def __str__(self):
        return f'{self.teacher.username} {self.class_name.name}'
    

    
class AttandanceSession(TimeStamp):

    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name= 'student_attandance')


    class Meta: 
        unique_together = ('teacher', 'class_name', 'subject', 'created_at')

class AttandanceRecord(models.Model):

    class AtdStatus(models.TextChoices):
        A = 'A', 'Absent'
        P = 'P', 'Present'

    atd_session = models.ForeignKey(AttandanceSession, on_delete=models.CASCADE, related_name='attandance_records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attandance_records')
    status  =  models.CharField(max_length=1, choices=AtdStatus)

    class Meta:
        unique_together = ('atd_session', 'student')
    
    def __str__(self):
        return f'{self.student.first_name}'


class AssignmentSubmission(TimeStamp):

    def assignment_upload_path(instance, filename):
        I = instance
        s = I.student.first_name
        cl  = I.assignment.class_name
        cl    = cl.name +( cl.section )
        sbj = I.assignment.subj.name
        return f'{cl}/{sbj}/{s}/{filename}'
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'ST'},  related_name='my_submissions')
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to=assignment_upload_path)

    def save(self,*args, **kwargs):
        assignment  = AssignmentSubmission.objects.filter(student=self.student, assignment = self.assignment)
        if assignment: 
            # delete the previous submission and add new one to the database 
            assignment.delete()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return  self.student.first_name 
    

    

















