from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=80,blank=True,null=True)
    artist = models.CharField(max_length=80,blank=True,null=True)
    musician = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return str(self.username)
    
class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=12)
    description = models.TextField()


    def __str__(self):
        return self.name
    
class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=50)
    language = models.CharField(max_length=50,blank=True,null=True)
    emotion = models.CharField(max_length=50,blank=True,null=True)
    musician = models.CharField(max_length=50,blank=True,null=True)
    image = models.ImageField(upload_to = "images")
    song = models.FileField(upload_to = "songs")

    def __str__(self):
        return self.name
    