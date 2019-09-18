from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'Users'

    def ready(self):
        import Users.signals # Import the signals in the class of the Model what will send those signals
