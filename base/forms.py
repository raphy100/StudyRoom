from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class myusercreationform(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        # Only include editable fields here; topic is handled manually in the views
        fields = ['name', 'description']
        # host and participants are intentionally omitted

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

