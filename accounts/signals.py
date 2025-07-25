
from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save, post_save
from guardian.shortcuts import assign_perm 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives,send_mail 
from django.template.loader import render_to_string




password_changed = Signal()
password_reset  = Signal()


@receiver(password_changed)
def password_change_confirmation_email(sender, **kwargs):

    
    email = sender.email

    subject = "You have successfuly created your account at my commnunity "
    text_messasge = "Hey thanx again to be a part of us "
    from_email = "mycommnunity@gmail.com"
    to = [f'{sender.email}']

    email_message = EmailMultiAlternatives(subject,text_messasge, from_email, to)
    context = {
        "username": sender.username, 
        'p_change': True

    }
    html_string = render_to_string('accounts/password_change_reset.html', context )

    email_message.attach_alternative(html_string,'text/html')
    email_message.send()

@receiver(password_reset)
def password_change_confirmation_email(sender, **kwargs):

    
    email = sender.email

    subject = "You have successfuly created your account at my commnunity "
    text_messasge = "Hey thanx again to be a part of us "
    from_email = "mycommnunity@gmail.com"
    to = [f'{sender.email}']

    email_message = EmailMultiAlternatives(subject,text_messasge, from_email, to)
    context = {
        "username": sender.username, 
        'p_change': False

    }
    html_string = render_to_string('accounts/password_change_reset.html', context )
    
    email_message.attach_alternative(html_string,'text/html')
    email_message.send()


# automating the the object level permission assingment to the user who owned that profile 
my_profile_permission_signal = Signal()
account_registration_signal = Signal()

@receiver(my_profile_permission_signal)
def  automate_profile_permission(sender, instance, *ars, **kwargs):

    user = sender
    if user.role=='ST':
        model = 'studentprofile'
    else:
        model= 'teacherprofile'
    
    ct = ContentType.objects.get(app_label = 'accounts', model=model)
    permission = Permission.objects.get(codename='my_profile', content_type_id = ct.id)    

    # assigning permission to the user 
    assign_perm(permission, user, instance)
    account_registration_signal.send(sender=sender)


@receiver(account_registration_signal)
def successful_registration(sender, *args, **kwargs):

    """ here we are  going to send the information to the user such as, there user id, password and other stff"""

    














