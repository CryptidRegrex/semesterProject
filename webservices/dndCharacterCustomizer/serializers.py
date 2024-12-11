from rest_framework import serializers
from .models import Character
from django.contrib.auth.models import User
from .models import Profile

# class CharacterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Character
#         fields = '__all__'

# # Default set to authorized, password we are ensuring this is a write only field. We ARE NOT GOING TO ALLOW READS FROM THIS FIELD
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     # Include fields from the related Profile model
#     email = serializers.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email']
#         extra_kwargs = {
#             'password': {'write_only': True}, 
#         }

#     def create(self, validated_data):
#         # Extract email from validated data
#         email = validated_data.pop('email')

#         # Create the User
#         user = User.objects.create_user(**validated_data)

#         # Create a Profile with the extracted email and default type
#         Profile.objects.create(user=user, email=email, type="AUTHORIZED")

#         return user