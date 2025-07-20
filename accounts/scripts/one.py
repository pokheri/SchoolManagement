
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from guardian.shortcuts import assign_perm
from .. models import StudentProfile
from django.contrib.contenttypes.models import ContentType



User = get_user_model()


def run():

    user = User.objects.get(username='Amma')
    profile = user.get_profile()
    c_type = ContentType.objects.get(app_label='accounts', model='studentprofile')
    permission = Permission.objects.get(codename='my_profile',content_type =c_type)
    assign_perm(permission, user,profile )

