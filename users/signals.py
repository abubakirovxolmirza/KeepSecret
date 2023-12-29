from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from .profile_pict import choicer

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, 'profile'):
            return

        profile = Profile.objects.create(
            user=instance,
            gender=instance.gender,
            fullname=instance.fullname,
            phone_number=instance.phone_number,
        )

        if profile.gender == 'Male':
            profile.profile_image = f'profile_images/Male/male{str(choicer())}.jpg'
        else:
            profile.profile_image = f'profile_images/Female/female{str(choicer())}.jpg'

        profile.save()


