from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()
    bio = models.TextField(blank=True)
    profile_img_file = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    major = models.CharField(max_length=100, blank=True)
    minor = models.CharField(max_length=100, blank=True)
    school = models.CharField(max_length=100)
    class_year = models.IntegerField(null=True, blank=True)  # Allow null and blank values

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    graphic = models.ImageField(upload_to='project/category/images/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    copy_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.username} (Topic: {self.topic.title}, Subject: {self.topic.parent_subject.name})"

class Comment(models.Model):
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
    image = models.ImageField(upload_to='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        """return a string representation of the status message object"""
        return f'{self.image} at {self.timestamp} for {self.category}'
    
