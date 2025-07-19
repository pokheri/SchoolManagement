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


class Subject(TimeStamp):

    subject_id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    # teacher 

    def __str__(self):
        return f'{self.subject_name}'
    
class Course(TimeStamp):

    course_id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    duration  = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.course_name}'

class Enrollment(TimeStamp):
    
    student = models.OneToOneField(User, limit_choices_to={'role': 'STU'}, on_delete=models.CASCADE, related_name='enrollments')
    class_room = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL,null=True,  related_name='student_enrolled')
    subjects = models.ManyToManyField(Subject)
    courses = models.ManyToManyField('Course')
 
    class Meta:
        unique_together = ('student', 'class_room')
    def __str__(self):
        return f'{self.student.first_name}, {self.class_room.class_name}'
    
class ClassRoom(TimeStamp):

    class_id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=50, unique=True)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'T'}, related_name='my_class')
    class_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Stu'})
    location  = models.TextField()

    def __str__(self):
        return f'Class {self.class_name}'
    
class Assignment( TimeStamp):


    def assignment_upload_path(instance, filename):
        return f'assignments/class_{instance.class_name.class_name}/{filename}'

    teacher   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subj = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    assignment_file = models.FileField(upload_to=assignment_upload_path)
    message = models.TextField(null=True, blank=True)
    last_date_sub  = models.DateTimeField()
    
    class Meta:
        unique_together = ('class_name', 'subj')

    def __str__(self):
        return f'Assignment {self.subj.subject_name}'
    
class TeacherAssignment(TimeStamp):

    teacher = models.ForeignKey(User, limit_choices_to={'role': 'T'}, on_delete=models.CASCADE)
    class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='teachers')
    subjects    = models.ManyToManyField(Subject,related_name='subject_teachers')
    
    def __str__(self):
        return f'{self.teacher.first_name} {self.teacher.last_name}'

    
class AttandanceSession(TimeStamp):

    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    t_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name= 'student_attandance')


    class Meta: 
        unique_together = ('teacher', 'class_name', 't_subject')

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


class SubjectMark(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()


class ExamMark(TimeStamp):

    student    = models.ForeignKey(User, limit_choices_to={'role': 'STU'}, on_delete=models.CASCADE, related_name='marks')
    s_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_marks = models.ManyToManyField(SubjectMark)


    class Meta:
        unique_together = ('student', 's_subject')
    def __str__(self):
        return f'{self.student.first_name} - {self.created_at}'
    
class AssignmentSubmission(TimeStamp):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_submissions')
    sub_assingment = models.ForeignKey(Assignment, on_delete = models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='assignment/students')



    def save(self,*args, **kwargs):
        student  = AssignmentSubmission.objects.filter(student=self.student, assignment = self.assignment)
        if student: 
            # delete the previous submission and add new one to the database 
            student.delete()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.created_at}'
    
class TimeTable(TimeStamp):

    klass = models.OneToOneField(ClassRoom, on_delete=models.CASCADE, related_name='timetable')
    time_table = models.FileField(upload_to = 'timetable/')


    def __str__(self):
        return f'{self.klass.class_name} time table '


















