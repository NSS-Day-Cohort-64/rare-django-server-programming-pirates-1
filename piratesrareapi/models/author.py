"""User model"""

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    profile_image_url = models.CharField(max_length=500)
    created_on = models.DateTimeField()
    active = models.BooleanField(default=True) #may need to remove, leaving in case we can't use the built in is_active

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
