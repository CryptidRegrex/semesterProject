from rest_framework import serializers
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    model = Character
    fields = '__all__'