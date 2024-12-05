from django import forms
from .models import Character, Campaign

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'background', 'charClass', 'gender', 'strength', 'dexterity', 'constitution', 
                  'intelligence', 'wisdom', 'charisma', 'hitPoints', 'maxHitPoints', 'armorClass', 'speed', 
                  'proficiencyBonus', 'level', 'experiencePoints']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name']

class AccessTokenForm(forms.Form):
    access_token = forms.CharField(max_length=255, label="Access Token")
    character = forms.ModelChoiceField(
        queryset=Character.objects.none(),  # Set dynamically in the view
        label="Select a Character",
    )

class UpdateCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'race', 'background', 'charClass', 'gender', 'strength', 'dexterity', 'constitution', 
                  'intelligence', 'wisdom', 'charisma', 'hitPoints', 'maxHitPoints', 'armorClass', 'speed', 
                  'proficiencyBonus', 'level', 'experiencePoints']