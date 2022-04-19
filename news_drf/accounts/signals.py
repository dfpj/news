import random

from django.dispatch import receiver
from django.db.models.signals import post_save

from .tasks import send_email
from .models import User, Verify, Profile


@receiver(post_save, sender=User)
def user_register_verifycode(sender, instance, **kwargs):
    if instance.is_active == False:
        verify_code = random.randint(1001, 9999)
        Verify.objects.create(email=instance.email, code=verify_code)
        send_email(email=instance.email, code=verify_code)
    elif instance.is_active == True and not instance.profile:
        profile = Profile.objects.create()
        user = User.objects.get(email=instance.email)
        user.profile = profile
        user.save()
