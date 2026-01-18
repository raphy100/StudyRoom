from email.message import Message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, myusercreationform

 
def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email) 
        except: 
            messages.error(request, 'User does not exist')
            user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Email OR password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = myusercreationform()
    if request.method == 'POST':
        form = myusercreationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # Provide a clearer message; field-specific errors are shown on the form
            messages.error(request, 'Registration failed. Please fix the errors below.')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |  
        Q(description__icontains=q)
    )
    # Provide a preview (first 5) for the sidebar and the full list for counts/links
    topics = Topic.objects.all()[0:5]
    topics_preview = topics[:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    return render (request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'topics_preview': topics_preview, 'rooms_count': rooms_count, 'room_messages': room_messages})

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    partcipants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # Add the posting user to the room participants so they appear on the participants page
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': partcipants}
    return render(request,'base/room.html', context)

def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

def participants(request, pk):
    """Display the participant list for a specific room."""
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    context = {'room': room, 'participants': participants}
    return render(request, 'base/participants.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        # Accept a typed topic name or an existing topic id/name from the form
        topic_value = request.POST.get('topic')
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, 'Room name is required')
            context = {'form': form, 'topics': topics}
            return render(request, 'base/room_form.html', context)

        topic_obj = None
        if topic_value:
            if topic_value.isdigit():
                try:
                    topic_obj = Topic.objects.get(id=int(topic_value))
                except Topic.DoesNotExist:
                    topic_obj, _ = Topic.objects.get_or_create(name=topic_value)
            else:
                topic_obj, _ = Topic.objects.get_or_create(name=topic_value)

        room = Room.objects.create(host=request.user, topic=topic_obj, name=name, description=description)
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

# Create your views here.
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
       return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        # Handle topic similar to createRoom: accept typed name or existing id
        topic_value = request.POST.get('topic')
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            messages.error(request, 'Room name is required')
            context = {'form': form, 'topics': topics, 'room': room}
            return render(request, 'base/room_form.html', context)

        topic_obj = None
        if topic_value:
            if topic_value.isdigit():
                try:
                    topic_obj = Topic.objects.get(id=int(topic_value))
                except Topic.DoesNotExist:
                    topic_obj, _ = Topic.objects.get_or_create(name=topic_value)
            else:
                topic_obj, _ = Topic.objects.get_or_create(name=topic_value)

        # Update fields on the existing room and save
        room.name = name
        room.description = description
        room.topic = topic_obj
        room.save()
        return redirect('home')

    context = {'form': form , 'topics': topics, 'room': room}
    return render (request, 'base/room_form.html', context )
@login_required(login_url='login')

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
       return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'object': room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
       return HttpResponse('You are not allowed here!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'object': message}
    return render(request, 'base/delete.html', context)


login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all().order_by('-created')
    return render(request, 'base/activity.html', {'room_messages': room_messages})