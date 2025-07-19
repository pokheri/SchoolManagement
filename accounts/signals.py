
from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives,send_mail 
from django.template.loader import render_to_string




password_changed = Signal()
password_reset  = Signal()



@receiver(post_save,sender=User)
def user_model_save(sender, instance, created, **kwargs):

    if created:

        email = instance.email

        subject = "You have successfuly created your account at my commnunity "
        text_messasge = "Hey thanx again to be a part of us "
        from_email = "mycommnunity@gmail.com"
        to = [f'{instance.email}']

        email_message = EmailMultiAlternatives(subject,text_messasge, from_email, to)
        html_string = render_to_string('accounts/account_created_email.html', {"username": instance.username})
        email_message.attach_alternative(html_string,'text/html')
        email_message.send()




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















