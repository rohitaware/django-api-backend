from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class MessageSerializer(serializers.ModelSerializer):
    # By making the user field read-only, we tell the serializer
    # not to expect it in the POST/PUT request body.
    # We use StringRelatedField to show the user's username in the API response.
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        # The 'user' field is now handled by the explicit definition above.
        # 'date' is usually handled by the model (e.g., auto_now_add=True).
        fields = ['id', 'user', 'message', 'date']
        read_only_fields = ['date']