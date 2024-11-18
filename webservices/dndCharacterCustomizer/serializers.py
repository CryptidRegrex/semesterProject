from rest_framework import serializers
from .models import Character
from .models import User

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'type']
        extra_kwargs = {
            'type': {'default': 'AUTHORIZED'}  # Default to 'AUTHORIZED'
        }