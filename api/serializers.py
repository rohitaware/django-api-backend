from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class MessageSerializer(serializers.ModelSerializer):
   
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'message', 'date']
        read_only_fields = ['date']