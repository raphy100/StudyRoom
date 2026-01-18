from rest_framework.serializers import ModelSerializer
from base.models import Room, Topic


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'