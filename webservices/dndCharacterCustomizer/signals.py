from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


"""Had some help from ChatGPT with this method
   The decorator specifies when a certain action happens on a specific maodel execute this

   The sender or User is sent, it's instance of the record, flag if the user was created during save(), and
   all other keyword arguments

   The point of this is so that when a user is created we also create a profile record related to the User
"""
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile for new users with the default "AUTHORIZED" type
        Profile.objects.create(user=instance, email=instance.email, type="AUTHORIZED")
    else:
        # Save the profile if the user is updated
        instance.profile.save()