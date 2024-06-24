from django.apps import AppConfig


class GymStaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Gym_Staff'

    def ready(self):
        import Gym_Staff.signals
