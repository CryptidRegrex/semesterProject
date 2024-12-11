#So I can administer the profile model
from django.contrib import admin
from django.http import Http404
from .models import Profile, Character, Campaign

"""Resigtration of the profile object on the admin page. 
    All elements of the profile object are returned to the list displayed on the page
"""
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'email')

"""Passes back the list to display of the characters on the site. 
   We want the admins to moderate images and names used to ensure no misues of site
"""
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

"""Lists the Campaign name's avaliable to the admin on the admin page
"""
@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name',)