from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
       if created:
          Profile.objects.create(user=instance).save()
    except Exception as err:
       print(f'Error creating user profile!\n{err}')