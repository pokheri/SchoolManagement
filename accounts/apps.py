from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):

        # this is the special method that is used to load  the model and perform the app realted work at the time of loading and thing like that 
        from accounts import signals

