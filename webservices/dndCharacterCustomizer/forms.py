from django import forms
from .models import Character, Campaign
from django.contrib.auth.models import User

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = [
            'name', 'race', 'background', 'charClass', 'gender',
            'strength', 'dexterity', 'constitution', 'intelligence',
            'wisdom', 'charisma', 'hitPoints', 'maxHitPoints',
            'armorClass', 'speed', 'proficiencyBonus', 'level',
            'experiencePoints', 'athletics', 'acrobatics', 'sleightOfHand',
            'stealth', 'arcana', 'history', 'investigation', 'nature',
            'religion', 'animalHandling', 'insight', 'medicine',
            'perception', 'survival', 'deception', 'intimidation',
            'performance', 'persuasion'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Character Name'}),
            'race': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Character Race'}),
            'background': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Character Background'}),
            'charClass': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Character Class'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'strength': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'dexterity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'constitution': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'intelligence': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'wisdom': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'charisma': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'hitPoints': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'maxHitPoints': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'armorClass': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
            'speed': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'proficiencyBonus': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'level': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
            'experiencePoints': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'athletics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acrobatics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sleightOfHand': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stealth': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'arcana': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'history': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'investigation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nature': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'religion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'animalHandling': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'insight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'medicine': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'perception': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'survival': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deception': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'intimidation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'performance': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'persuasion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


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
        fields = [
            'name', 'race', 'background', 'charClass', 'strength', 'dexterity', 
            'constitution', 'intelligence', 'wisdom', 'charisma', 'hitPoints',
            'maxHitPoints', 'armorClass', 'speed', 'proficiencyBonus', 'level',
            'athletics', 'acrobatics', 'sleightOfHand', 'stealth', 'arcana', 
            'history', 'investigation', 'nature', 'religion', 'animalHandling', 
            'insight', 'medicine', 'perception', 'survival', 'deception', 
            'intimidation', 'performance', 'persuasion'
        ]

class CharacterImageUploadForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            max_size = 20 * 1024 * 1024  # 20MB
            valid_mime_types = ['image/jpeg', 'image/png']
            valid_extensions = ['jpg', 'jpeg', 'png']

            # Check file size
            if image.size > max_size:
                raise forms.ValidationError("File size must be less than 20MB.")

            # Check file type
            if image.content_type not in valid_mime_types:
                raise forms.ValidationError(f"Unsupported file type. Only {', '.join(valid_extensions)} are allowed.")

        return image


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


    #ChatGPT helped me figure out how the heck this works. I failed to understand django's doc.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email