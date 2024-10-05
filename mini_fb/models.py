# mini_fb/models.py

from django.db import models

# Create your models here.

class Profile(models.Model):
    """encapsulate the idea of a Profile"""

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_img_url = models.TextField(blank=False)

    def __str__(self):
        """return a string representation of this profile object."""
        return f'{self.first_name} {self.last_name} at {self.city} at {self.email_address}'

