# mini_fb/models.py

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Create your models here.

class Profile(models.Model):
    """encapsulate the idea of a Profile"""

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    birth_date = models.DateField(null=True, blank=False)

    # i wanted a choice between url or image cause the discord urls expired :3
    profile_img_url = models.URLField(blank=True, null=True)    # optional URL
    profile_img_file = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        """return a string representation of this profile object."""
        return f'{self.first_name} {self.last_name} at {self.city} at {self.email_address}'
    
    def get_status_messages(self):
        """Return all status messages for this profile, ordered by timestamp."""
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        """return the url to view this profile object"""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_profile_image(self):
        """Return the uploaded image if it exists, otherwise return the URL."""
        if self.profile_img_file and hasattr(self.profile_img_file, 'url'):
            return self.profile_img_file.url  # Use the uploaded image
        elif self.profile_img_url is not None:
            return self.profile_img_url  # Use the URL if no file is uploaded
        else:
            return '/media/profile_images/default_pfp.jpg'  # No image provided
        
    def get_friend_suggestions(self):
        '''Return a list of Profiles that are not friends with this Profile'''
        # Get all the profiles excluding self
        all_profiles = Profile.objects.exclude(pk=self.pk)

        # Get the IDs of current friends
        friend_ids = set(
            friend.pk for friend in self.get_friends()
        )

        # Filter out profiles that are already friends
        suggestions = all_profiles.exclude(pk__in=friend_ids)

        return list(suggestions)

    def get_friends(self):
        '''Return all friends of this profile'''
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        # Combine both sets of friends
        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)

        # the actual Profile objects
        friends = Profile.objects.filter(pk__in=friend_ids)
        return list(friends)    # make sure we return a list
    
    def add_friend(self, other):
        '''Add a Friend relation between self and other, if not already present'''
        # Prevent self-friending
        if self == other:
            raise ValidationError("A user cannot be friends with themselves.")

        # Check for an existing friendship in either direction
        friendship_exists = Friend.objects.filter(
            (models.Q(profile1=self) & models.Q(profile2=other)) |
            (models.Q(profile1=other) & models.Q(profile2=self))
        ).exists()

        if not friendship_exists:
            # If no existing friendship, create one
            Friend.objects.create(profile1=self, profile2=other)

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
      
    def get_images(self):
        """return all images for this status message"""
        return self.image_set.all()
    
class Image(models.Model):
    ''' encapsulates the idea of an image file (not a URL) that is stored 
    in the Django media directory 
    image field, a foreign key to connect to status messages (to include zero
    to as many imagesm in a status message), timestamp'''
    image = models.ImageField(upload_to='')
    message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        """return a string representation of the status message object"""
        return f'{self.image} at {self.timestamp} for {self.message}'

class Friend(models.Model):
    '''Encapsulate a friendship between two profiles '''
    profile1 = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='profile1'
    )
    profile2 = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='profile2'
    )
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        '''Return a string representation of the friendship.'''
        return f'{self.profile1} & {self.profile2}'