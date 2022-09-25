# model configation written in here

from email.policy import default
from pyexpat import model
from django.db import models
# django already has a built-in User class
from django.contrib.auth.models import AbstractUser
# Create your models here.
# from .managers import UserManager

class User(AbstractUser):
    name = models.CharField(max_length=200, null = True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null= True, default = 'avatar.svg')
    # objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    # automatically set unique id for every single instance
    # models.SET_NULL means not deleting the model even if the parent class deleted
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete= models.SET_NULL, null=True)
    # user has many rooms that they participates in, room has many user they are paticipate to room itself
    # room has host(User relationship), that's because we need related_name
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    name = models.CharField(max_length=200)
    # when created a model instace, it won't raise any error even if the attribute wasn't given, null = True
    # when submitted a form, it won't also raise any error even if the attribute wasn't given, blank = True
    discription = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add = just first fime, instance created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ['-updated'] '-' means descendent
        ordering = ['-updated','-created']

    

### this method defines the outputs of this model which shown when this models called or invoked by print() method, if this function was not set, __repr__ method invoked and represents the pure info of the object
    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete= models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering = ['-updated','-created']

    def __str__(self) -> str:
        return self.body[:50]
        
