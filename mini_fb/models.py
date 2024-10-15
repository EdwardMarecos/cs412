# mini_fb/models.py

from django.db import models

# Create your models here.

class Profile(models.Model):
    """encapsulate the idea of a Profile"""

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    profile_img_url = models.TextField(blank=False)

    def __str__(self):
        """return a string representation of this profile object."""
        return f'{self.first_name} {self.last_name} at {self.city} at {self.email_address}'
    
    def get_status_messages(self):
        """Return all status messages for this profile, ordered by timestamp."""
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')

class StatusMessage(models.Model):
    ''' model the data attributes of Facebook status message. 
    This StatusMessage model will need to include the following 
    data attributes:
        timestamp (the time at which this status message was created/saved)
        message (the text of the status message)
        profile (the foreign key to indicate the relationship to the Profile 
            of the creator of this message)'''
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        """return a string representation of the status message object"""
        return f'{self.message} at {self.timestamp} for {self.profile}'