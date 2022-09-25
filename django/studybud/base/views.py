# when users went to any urls, this file will fire off quieries to model for database stuff
# or render some pages 
# specific functions or classes are asighed  for each urls

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message,User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm, UserForm,MyUserCreationForm

# Create your views here.

# rooms = [
#     { 'id':1, 'name':'study with me'},
#     { 'id':2, 'name':'draw with me'},
#     { 'id':3, 'name':'play mucic with me'}
# ]

# {'rooms':rooms}
# key means to specifiy how is the variable called on tamplates
# user puts url -> call function from url -> render html from template
# value represents valuables

# project_name/urls.py includes "base/" then in "setting.py" set templates "BASE_DIR/ "templates", then in base/views.py rendered "base/*.html"
# we can reach to base/templates/base/*.html

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        pass_word = request.POST.get('password')

        try:
            # username = attribute of User class, user_name = a value from POST method 
            user = User.objects.get(email = email)

        except:
            # messages.type(request -> to know where to show a message, 'message')
            messages.error(request, 'user is not found')
        
        # authenticate returns either an user object that matches the cridential / None
        user = authenticate(request, email = email, password=pass_word)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'email or password is not correct')
    context = {'page':page}
    return render(request, 'base/login_resister.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def resister_user(request):
    #doesn't need page variable, cause it'll be dealed with else statement
    # page = 'resister'
    form = MyUserCreationForm()
    if request.method == 'POST':
        # created a form from user input
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            # user instance create from form data
            # commit=False, we wanna add in more data to the instance we'll create
            user = form.save(commit=False)
            user.username = user.username.lower()
            #save instance
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'error occured during resistration')
    context = {'form' : form}
    return render(request, 'base/login_resister.html', context)

def user_profile(request, pk):

    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    # rooms = user.room_set.filter(
    #     Q(topic__name__icontains = q)|
    #     Q(name__icontains = q)|
    #     Q(discription__icontains = q)
    #     )
    # for filtering messages in active feed as the main feed's rooms get filtered
    room_messages = user.message_set.all()
    # room_messages = user.message_set.filter(Q(room__topic__name__icontains = q))

    context = {'user':user, 'topics':topics, 'rooms':rooms, 'room_messages':room_messages}
    return render(request, 'base/user_profile.html',  context)

def home(request):
    # method = GET, gives us url, then get 'q= topic_name'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()[0:5]
    #filter by foreignkey of name(Attribute of topic) of topic, get foreign key of topic -> then get topic name of that topic
    # icontains return posivive, if the given value contained in object, if None, return everything
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q) |
        Q(discription__icontains = q)
    )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count, 'room_messages':room_messages}
    return render(request, "base/home.html", context)

# room(request,pk) means given url like room/**, render base/room.html whatever value is in **
def room(request, pk):

    # when given url "room/1,2,3", loop through list of dictionaries(rooms), then if primary key(1/2/3) matches any id, throw back a dictionary,
    # room = None
    # for i in rooms:
    #     if int(pk) == i['id']:
    #         room = i
    #         context = {'room':room}

    # given url room/pk(1/2...), specify the instance of room, and give it to the template
    room = Room.objects.get(id = pk)
        # get instances of childrens class
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, "base/room.html", context)

# login_url equals to 'url name'
@login_required(login_url='login_page')
def createroom(request):
    form = RoomForm()
    # get form for room
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')

        # if given topic_name is not created earlier, create
        # if it already exists, just get it from instances
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            discription = request.POST.get('discription')
        )
        # if form.is_valid():
        #     # commit=False, we wanna add in more data to the instance we'll create
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request, "base/room_create.html", context)

@login_required(login_url='login_page')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    # for update, we need to specify which room should be shown
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # restrict other users manipulate another user's room
    if request.user != room.host:
        return HttpResponse('You are not allowed')


    if request.method == "POST":
        topic_name = request.POST.get('topic')
        # if given attribute is not in the data, then create
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.host = request.user
        room.name = request.POST.get('name')
        room.discription = request.POST.get('discription')
        room.topic = topic
        room.save()
        
    # for update, we need to specify which room's data should be saved
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, "base/room_create.html", context)


@login_required(login_url='login_page')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    # obj, we use delete.html for deleting anything
    return render(request, "base/delete.html", {'obj': room})

@login_required(login_url='login_page')
def deletemessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    # obj, we use delete.html for deleting anything
    return render(request, "base/delete.html", {'obj': message})

@login_required(login_url='login_page')
def usersetting(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk = user.id)

    context = {'form':form}
    return render(request,'base/settings.html', context)

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)

def activity(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)