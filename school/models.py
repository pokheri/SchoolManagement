from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
User = settings.AUTH_USER_MODEL


class TimeStamp(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    update_at  = models.DateField(auto_now=True)
    
    class Meta:
        abstract = True

class ActionStatus(models.TextChoices):

    P = 'P', 'Pending'
    F = 'F', 'Fail'

class PaymentMethod(models.TextChoices):

    ONLINE = 'Online'
    CASH = 'Cash'
    CARD = 'Card'

class SchoolClass(TimeStamp):

    class SectionChoice(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'

    name = models.CharField(max_length=50)
    section  = models.CharField(max_length=1, choices=SectionChoice)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'T'}, related_name='my_class')
    # class_coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Stu'})
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
                                    violation_error_message="Teacher already assingned asingment to this class ")
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
                                     violation_error_message='Teacher is already assigned to the class ' )
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

        assignment = AssignmentSubmission.objects.update_or_create(
            student = self.student, assignment  = self.assignment
        )
        assignment.file = self.file
        assignment.save()

    
    def __str__(self):
        return  self.student.first_name 
    

class Examination(models.Model):

    title = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date   = models.DateField()

    def __str__(self):
        return f'{self.title } {self.start_date} to {self.end_date }'


# subject marks per exam 
class SubjectMarks(TimeStamp):

    exam = models.ForeignKey(Examination, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=100)
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['exam', 'subject'], name='subject_name_must_unique_for_examintion', violation_error_message="This is becuase Thsi subject is already register ")
        ]
    def __str__(self):
        return f'{self.exam.title},{self.subject.name} {self.total_marks}'
    
class ExamMarks(TimeStamp):

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    acadmic_year = models.CharField(max_length=10)
    subject_marks   = models.ForeignKey(SubjectMarks, on_delete=models.CASCADE)
    obtain_marks = models.FloatField()
    student_status = models.CharField(max_length=20, default='PASS')
    grade = models.CharField(max_length=1)
    
    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['student', 'subject_marks'], name='student_and_exam_is_unique', violation_error_message='Student marks already updated with this subject')
        ]
    
    def save(self,*args, **kwargs):

        percentage =  (self.obtain_marks / self.subject_marks.total_marks) * 100
        
        match percentage:
            case p if p >=90:
                self.grade = 'A'
            case p if p >=80:
                self.grade = 'B'
            case p if p >=60:
                self.grade = 'C'
            case p if p < 60:
                self.grade = 'D'
            case p if p < 33:
                self.student_status = 'FAIL'
    
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f'{self.student.first_name} obtain {self.obtain_marks} in {self.subject_marks.subject.name}'

# request documents and will only, receive in shcool 
class DocStatus(models.TextChoices):
    A = 'A', 'Accept'
    R = 'R', 'Reject'
    W = 'W', 'Waiting'


class Document(TimeStamp):
    
    class DocChoice(models.TextChoices):

        BO = 'BO', 'Bonafied Certificate'
        SC = 'SC', 'School Leaving Certificate '
        CH = 'CH', 'Character Certificate '
        OT = 'OT', 'Others'

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_requests')
    status = models.TextField(max_length=2, choices=DocStatus, default=DocStatus.W)
    doc_type = models.TextField(max_length=2, choices=DocChoice)
    message = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.student.full_name} requested {self.get_doc_type_display()} on {self.created_at}'
    # def student_clean(self):

        
    #     student = Document.objects.filter(student = self.student, doc_type=self.doc_type)[0]
    #     if student and student.status=='A':
    #         self.a

# leave reqeust to the class teacher 
class LeaveRequest(TimeStamp):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_request')
    application = models.FileField(upload_to='application/')
    message = models.TextField(null=True, blank=True)
    status = models.TextField(max_length=2, choices=DocStatus, default=DocStatus.W)

    def __str__(self):
        return f'{self.student.full_name} request leave on {self.created_at}'
    class Meta: 
        ordering = ['pk']

class WeekDay(models.TextChoices):
        MON = 'Mon', 'Monday'
        TUE = 'Tue', 'Tuesday'
        WED = 'Wed', 'Wednesday'
        THU = 'Thu', 'Thursday'
        FRI = 'Fri', 'Friday'
        SAT = 'Sat', 'Saturday'

class AbstractTimeTable(models.Model):

    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    acadmic_year = models.TextField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=3, choices=WeekDay.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ['class_name', 'weekday', 'start_time']
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.class_name.name}{self.class_name.section} | {self.weekday} {self.start_time} - {self.end_time} | {self.subject.name}"



class SubjectTimeTable(AbstractTimeTable):

    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'T'})

class ExamTimeTable(AbstractTimeTable):
    pass

class Event(TimeStamp):

    title = models.TextField(max_length=200)
    date = models.DateField()
    start_time= models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    message = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'date'], name='event_and_date_is_unique', violation_error_message="Event with this title and date is already registerd ")
        ]

    def __str__(self):
        return f'{self.title[:50]} on {self.date}'
    
class FeeStructure(models.Model):

    class_name = models.OneToOneField(SchoolClass, on_delete=models.CASCADE, related_name='fee_structure')
    tuestion_fee = models.FloatField()
    exam_fee = models.FloatField(default=0)
    extra  = models.FloatField(default=0)

    @property
    def get_total_amount(self): #per month 
        
        return self.tuestion_fee + self.exam_fee + self.extra

    def __str__(self):
        return f'{self.class_name.name} fee structure '
    

class StudentFeeRecord(TimeStamp):
    
    class MonthsChoice(models.TextChoices):
        JAN = 'JAN'
        FEB = 'FEB' 
        MAR = 'MAR'
        APR  = 'APR'
        MAY = 'MAY'
        JUN = 'JUN'
        AUG = 'AUG'
        SEP = 'SEP' 
        OCT = 'OCT'
        NOV = 'NOV'
        DEC = 'DEC'

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee_records')
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=3,  choices=MonthsChoice)   
    year = models.IntegerField(blank=True)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod)
    paid  = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'month'], name='student_and_month_must_unique', violation_error_message='fee already paid for this month ')
        ]

    def save(self, *args, **kwargs ):

        if not self.year:
            self.year = datetime.now().year 

    def __str__(self):
        return f'{self.student.full_name}-{self.month}-{self.paid}'
    

class TransportRecord(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'ST'}, related_name='transport')
    route_name = models.CharField(max_length=100)
    fee = models.FloatField()
    is_active = models.BooleanField(default=True)


# class BookIssue(models.Model):
    
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     issued_on = models.DateField(auto_now_add=True)
#     return_due = models.DateField()
#     returned = models.BooleanField(default=False)


    





    

















