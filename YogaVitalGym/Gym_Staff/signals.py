from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Gym_Staff_Data

@receiver(post_save, sender=User)
def create_staff(sender, instance, created, **kwargs):
    if created:
        Gym_Staff_Data.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_staff(sender, instance, **kwargs):
    instance.staff.save()
