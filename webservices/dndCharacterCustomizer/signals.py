from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

#This essentially meets some criteria and then the dectoractor will validate that the criteria is met AND the function executes. 
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile for new users with the default "AUTHORIZED" type
        Profile.objects.create(user=instance, email=instance.email, type="AUTHORIZED")
    else:
        # Save the profile if the user is updated
        instance.profile.save()