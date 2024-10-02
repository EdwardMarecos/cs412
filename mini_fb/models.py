from django.db import models

# Create your models here.

class Profile(models.Model):
    """encapsulate the idea of a Profile"""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    email_address = models.CharField(max_length=30)
    profile_img_url = models.CharField(max_length=90)

