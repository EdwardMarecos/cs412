# File: models.py
# Author: Edward Marecos (emarecos@bu.edu), 12/1/2024
# Description: Contains all the model classes for the project app. These models define the database structure and relationships for the Profile, Category, Subject, Topic, Note, Comment, and Image models.

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class Profile(models.Model):
    """Model to represent a user's profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()
    bio = models.TextField(blank=True)
    profile_img_file = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    minor = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100)
    class_year = models.IntegerField(null=True, blank=True)  # Allow null and blank values

    def get_pfp(self):
        """Return the uploaded image if it exists, otherwise return the URL."""
        if self.profile_img_file and hasattr(self.profile_img_file, 'url'):
            return self.profile_img_file.url  # Use the uploaded image
        else:
            return '/media/profile_images/default_pfp.jpg'  # No image provided

    def is_following(self, profile):
        """Check if this profile is following another profile."""
        return profile in self.following.all()

    def is_followed_by(self, profile):
        """Check if this profile is followed by another profile."""
        return profile in self.followers.all()

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"

class Category(models.Model):
    """Model to represent a category."""
    name = models.CharField(max_length=255, unique=True)
    graphic = models.ImageField(upload_to='project/category/images/', null=True, blank=True)
    
    def __str__(self):
        """Return a string representation of the cat."""
        return self.name

class Subject(models.Model):
    """Model to represent a subject, which is linked to a category."""
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the subject."""
        return f"{self.name} ({self.category.name})"

class Topic(models.Model):
    """Model to represent a topic, which is linked to a subject."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the topic."""
        return self.title

class Note(models.Model):
    """Model to represent a note, which is linked to a topic and an author."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    copy_count = models.PositiveIntegerField(default=0)

    # New ManyToManyField to track likes and bookmarks
    liked_by = models.ManyToManyField(Profile, related_name="liked_notes", blank=True)
    bookmarked_by = models.ManyToManyField(Profile, related_name="bookmarked_notes", blank=True)

    def like(self, profile):
        """Like the note, updating the like count."""
        self.liked_by.add(profile)
        self.like_count = self.liked_by.count()
        self.save()

    def unlike(self, profile):
        """Unlike the note, updating the like count."""
        self.liked_by.remove(profile)
        self.like_count = self.liked_by.count()
        self.save()

    def bookmark(self, profile):
        """Adds a bookmark from a profile."""
        self.bookmarked_by.add(profile)
        self.bookmark_count = self.bookmarked_by.count()
        self.save()

    def unbookmark(self, profile):
        """Removes a bookmark from a profile."""
        self.bookmarked_by.remove(profile)
        self.bookmark_count = self.bookmarked_by.count()
        self.save()

    def __str__(self):
        return f"{self.title} by {self.author.user.username} (Likes: {self.like_count}, Bookmarks: {self.bookmark_count})"

class Comment(models.Model):
    """Model to represent a comment on a note."""
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user} on {self.note}'

class Image(models.Model):
    ''' encapsulates the idea of an image file (not a URL) that is stored 
    in the Django media directory 
    image field, a foreign key to connect to status messages (to include zero
    to as many imagesm in a status message), timestamp'''
    # i ended up not using it but im not about to risk something breaking so it stays here
    image = models.ImageField(upload_to='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        """return a string representation of the status message object"""
        return f'{self.image} at {self.timestamp} for {self.category}'
    
