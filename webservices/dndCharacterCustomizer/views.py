#Using the decorator to make is simple
#If a user tries to access this page without authentication it will redirect them
#If the user IS logged in it will execute the definition
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Character, Campaign
#This took forever to figure out. Essentially we are going to call django's native login() function and we are going to rename it to make it clear what it is
#used within login_view definition
from django.contrib.auth import authenticate, login as auth_login
from django.http import Http404
from .forms import CharacterForm, CampaignForm, AccessTokenForm, CharacterImageUploadForm, UpdateCharacterForm
import random

# Index view for the home page when I render the initial page
def index(request):
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    context = {
        'num_visits': num_visits
    }
    return render(request, 'index.html', context=context)

# This will render the login.html page so users can attempt to authenticate to the application
def login_view(request):
    #Based on the request we'll authenticate 
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Use Django's built-in login function
            return redirect("user_dashboard")  # Redirect to the user's dashboard
        else:
            return render(request, "login.html", {"error": "Invalid username or password."})
    
    return render(request, "login.html")

@login_required
def character_detail(request, character_id):
    # Get the character, ensuring it belongs to the logged-in user
    character = get_object_or_404(Character, id=character_id, profiles__user=request.user)

    # Initialize forms
    image_upload_form = CharacterImageUploadForm(instance=character)
    update_character_form = UpdateCharacterForm(instance=character)

    if request.method == "POST":
        if "upload_image" in request.POST:
            # Handle image upload
            image_upload_form = CharacterImageUploadForm(request.POST, request.FILES, instance=character)
            if image_upload_form.is_valid():
                image_upload_form.save()
                messages.success(request, "Image uploaded successfully!")
            else:
                messages.error(request, "Failed to upload image. Please try again.")
        elif "delete_image" in request.POST:
            # Handle image deletion
            if character.image:
                character.image.delete()  # Deletes the file from storage
                character.image = None
                character.save()
                messages.success(request, "Image deleted successfully!")
            else:
                messages.error(request, "No image to delete.")
        elif "update_character" in request.POST:
            # Handle character update
            update_character_form = UpdateCharacterForm(request.POST, instance=character)
            if update_character_form.is_valid():
                update_character_form.save()
                messages.success(request, f"Character '{character.name}' updated successfully.")
            else:
                messages.error(request, "Failed to update character. Please fix the errors below.")
        elif "join_campaign" in request.POST:
            # Handle joining a campaign
            campaign_token = request.POST.get("campaign_token")
            campaign = Campaign.objects.filter(access_token=campaign_token).first()
            if campaign:
                if campaign not in character.campaigns.all():
                    character.campaigns.add(campaign)
                    messages.success(request, f"Character '{character.name}' successfully joined the campaign '{campaign.name}'.")
                else:
                    messages.info(request, f"Character '{character.name}' is already part of the campaign '{campaign.name}'.")
            else:
                messages.error(request, "Invalid campaign token. Please try again.")
        return redirect("character_detail", character_id=character.id)

    # Fetch campaigns the character is part of
    campaigns = character.campaigns.all()

    return render(request, "character_detail.html", {
        "character": character,
        "image_upload_form": image_upload_form,
        "update_character_form": update_character_form,
        "campaigns": campaigns,
    })




@login_required
def user_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    
    # Campaigns owned by the user
    owned_campaigns = profile.campaign_profiles.all()
    
    # Characters created by the user
    created_characters = profile.owners.all()

    # Characters associated with campaigns owned by the user
    associated_characters = Character.objects.filter(
        campaigns__userOwner=profile
    ).exclude(profiles=profile).distinct()

    # Messages for empty data
    campaigns_message = "No Campaigns" if not owned_campaigns else None
    created_characters_message = "No Created Characters" if not created_characters else None
    associated_characters_message = "No Associated Characters" if not associated_characters else None

    # Initialize forms
    character_form = CharacterForm()
    campaign_form = CampaignForm()
    token_form = AccessTokenForm()
    token_form.fields['character'].queryset = created_characters

    # Prepare image upload forms for each created character
    character_image_forms = [
        (character, CharacterImageUploadForm(instance=character))
        for character in created_characters
    ]

    if request.method == "POST":
        if 'create_character' in request.POST:  # Create a new character
            character_form = CharacterForm(request.POST)
            if character_form.is_valid():
                new_character = character_form.save(commit=False)
                new_character.save()
                new_character.profiles.add(profile)  # Associate with the user's profile
                return redirect('user_dashboard')

        elif 'randomize_character' in request.POST:
            randomized_data = randomize_character()
            new_character = Character.objects.create(**randomized_data)
            new_character.profiles.add(profile)
            new_character.save()
            messages.success(request, f"Character '{new_character.name}' created successfully!")
            return redirect('user_dashboard')
        
        elif 'create_campaign' in request.POST:  # Create a new campaign
            campaign_form = CampaignForm(request.POST)
            if campaign_form.is_valid():
                new_campaign = campaign_form.save(commit=False)
                new_campaign.userOwner = profile  # Set campaign owner
                new_campaign.save()
                new_campaign.profiles.add(profile)  # Add to user's accessible campaigns
                return redirect('user_dashboard')
        
        elif 'submit_token' in request.POST:  # Handle access token submission
            token_form = AccessTokenForm(request.POST)
            token_form.fields['character'].queryset = created_characters
            if token_form.is_valid():
                access_token = token_form.cleaned_data['access_token']
                character = token_form.cleaned_data['character']
                campaign = get_object_or_404(Campaign, access_token=access_token)

                # Add the character to the campaign
                if character not in campaign.characters.all():
                    campaign.characters.add(character)
                    campaign.save()
                    messages.success(request, f"{character.name} has been added to the campaign: {campaign.name}.")
                else:
                    messages.info(request, f"The character is already part of the campaign: {campaign.name}.")
                return redirect('user_dashboard')

        elif 'upload_image' in request.POST:  # Handle image upload
            character_id = request.POST.get('character_id')  # Get the character ID
            character = get_object_or_404(Character, id=character_id, profiles=profile)
            form = CharacterImageUploadForm(request.POST, request.FILES, instance=character)
            if form.is_valid():
                form.save()  # Save the form if valid
                messages.success(request, f"Image uploaded for character '{character.name}'.")
            else:
                messages.error(request, f"Failed to upload image: {form.errors}")
            return redirect('user_dashboard')
        
        elif 'delete_character' in request.POST:  # Handle character deletion
            character_id = request.POST.get('character_id')
            character = get_object_or_404(Character, id=character_id, profiles=profile)
            character.delete()
            messages.success(request, f"Character '{character.name}' has been deleted.")
            return redirect('user_dashboard')

    return render(request, 'dashboard.html', {
        'profile': profile,
        'campaigns': owned_campaigns,
        'created_characters': created_characters,
        'associated_characters': associated_characters,
        'campaigns_message': campaigns_message,
        'created_characters_message': created_characters_message,
        'associated_characters_message': associated_characters_message,
        'character_form': character_form,
        'campaign_form': campaign_form,
        'token_form': token_form,
        'character_image_forms': character_image_forms,  # Pass image forms to template
    })




@login_required
def update_character(request, character_id):
    # Fetch the character
    character = get_object_or_404(Character, id=character_id)

    # Check if the logged-in user owns a campaign associated with this character
    profile = Profile.objects.get(user=request.user)
    if not Campaign.objects.filter(userOwner=profile, characters=character).exists():
        return HttpResponseForbidden("You do not have permission to update this character.")

    # Process the form
    if request.method == "POST":
        form = UpdateCharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            messages.success(request, f"Character '{character.name}' updated successfully.")
            return redirect('user_dashboard')
    else:
        form = UpdateCharacterForm(instance=character)

    return render(request, 'update_character.html', {
        'form': form,
        'character': character,
    })


def logout_view(request):
    logout(request)  # Log out the user
    return redirect("login")  # Redirect to login page

#To note here the signal will process the creation of a profile record. 
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        errors = []
        
        # Validate passwords
        if password1 != password2:
            errors.append("Passwords do not match.")
        
        # Check if username is taken
        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken.")
        
        # Check if email is taken
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")
        
        if errors:
            return render(request, "register.html", {"errors": errors})
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, "Your account has been created! You can now log in.")
        return redirect("login")
    
    return render(request, "register.html")

# Add a character to a user's profile
def add_character_to_profile(user, character_id):
    profile = user.profile
    character = Character.objects.get(id=character_id)
    profile.characters.add(character)

# Add a campaign to a user's profile
def add_campaign_to_profile(user, campaign_id):
    profile = user.profile
    campaign = Campaign.objects.get(id=campaign_id)
    profile.campaigns.add(campaign)


#Helper methods
def randomize_character():
    races = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling", "Gnome", "Half-Orc", "Half-Elf"]
    backgrounds = ["Soldier", "Noble", "Urchin", "Sage", "Criminal", "Folk Hero"]
    classes = ["Fighter", "Wizard", "Rogue", "Cleric", "Paladin", "Ranger", "Bard"]
    ability_scores = sorted([random.randint(3, 18) for _ in range(6)], reverse=True)  # Randomly roll six scores
    
    return {
        "name": f"Random Character {random.randint(1, 1000)}",
        "race": random.choice(races),
        "background": random.choice(backgrounds),
        "charClass": random.choice(classes),
        "strength": ability_scores[0],
        "dexterity": ability_scores[1],
        "constitution": ability_scores[2],
        "intelligence": ability_scores[3],
        "wisdom": ability_scores[4],
        "charisma": ability_scores[5],
        "hitPoints": random.randint(5, 15),  # Example starting range
        "maxHitPoints": random.randint(10, 20),
        "armorClass": random.randint(10, 18),
        "speed": 30,  # Standard speed for most characters
        "proficiencyBonus": 2,  # Default for level 1
        "level": 1,  # Start at level 1
    }