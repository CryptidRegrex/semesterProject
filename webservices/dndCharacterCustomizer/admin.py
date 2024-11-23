from django.contrib import admin

# Register your models here.

#So I can administer the profile model
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'email')