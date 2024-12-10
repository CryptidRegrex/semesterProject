#So I can administer the profile model
from django.contrib import admin
from django.http import Http404
from .models import Profile, Character, Campaign

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'email')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name',)