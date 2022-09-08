# when users went to any urls, this file will fire off quieries to model for database stuff
# or render some pages 
# specific functions or classes are asighed  for each urls

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "home.html")

def room(request):
    return render(request, "room.html")
    