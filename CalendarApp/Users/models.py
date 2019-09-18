from django.db import models
from django.contrib.auth.models import User

#Note:
#   Each model is a Python class that subclasses django.db.models.Model.
#   Each attribute of the model represents a database field.
#   A model is the single, definitive source of information about your data. 
#   It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.
class Profile(models.Model):
    # Every profile is going to be related to one user only, hence there is a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Cascade deletes. Django emulates the behavior of the SQL constraint ON DELETE CASCADE and also deletes the object containing the ForeignKey.
                                                                # If the user gets deleted, its profile will also get deleted

    def __str__(self): # This method returns the string representation of the object. This method is called when print() or str() function is invoked on an object.
        return f'{self.user.username}'

    