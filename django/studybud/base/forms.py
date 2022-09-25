from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class RoomForm(ModelForm):
    class Meta:
        # which model is this form for 
        model = Room
        # which attributes does this form include
        fields = '__all__'
        # no need for letting host be able to enter host's name and participants during creating room
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User

        fields = ['name','username','email', 'bio', 'avatar']