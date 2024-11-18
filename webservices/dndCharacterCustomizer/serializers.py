from rest_framework import serializers
from .models import Character
from .models import User

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

# Default set to authorized, password we are ensuring this is a write only field. We ARE NOT GOING TO ALLOW READS FROM THIS FIELD
# Security first LOL
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'type']
        extra_kwargs = {
            'type': {'default': 'AUTHORIZED'}  
        }