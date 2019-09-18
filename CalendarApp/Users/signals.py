from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# When a user is created, we want a profile for that user to also be created
# post_save is sent at the end of the save() method of the model(in this case the User model).


#Note:
# sender   - The model class.
# instance - The actual instance being saved.
# created  - A boolean; True if a new record was created.
# **kwargs - accepts any additional arguments
@receiver(post_save, sender=User) #Thanks to the receiver decorator, the create_profile function will only called when a User is saved 
def create_profile(sender, instance, created, **kwargs): 
    if created: # If the user was created 
        Profile.objects.create(user=instance) #then create a profile instance with the User object that was passed in
    

@receiver(post_save, sender=User) #Thanks to the receiver, the save_profile funtion will only be called when a User is saved
def save_profile(sender, instance, **kwargs): # No need to check if the user is created, just save it 
    instance.profile.save() # We want to save the profile instance of that User whenever the User is saved