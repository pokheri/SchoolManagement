
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from guardian.shortcuts import assign_perm
from .. models import StudentProfile
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser


User = get_user_model()


def run():

    print('hello how are you doing ')
