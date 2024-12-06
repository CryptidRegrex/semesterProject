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
from .forms import CharacterForm, CampaignForm, AccessTokenForm, CharacterImageUploadForm

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

#Using the decorator to make is simple
#If a user tries to access this page without authentication it will redirect them
#If the user IS logged in it will execute the definition
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CharacterForm, CampaignForm, AccessTokenForm, UpdateCharacterForm
from .models import Profile, Campaign, Character

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Character, Campaign
from .forms import CharacterForm, CampaignForm, AccessTokenForm, CharacterImageUploadForm

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

    # Prepare image upload forms for each created character
    character_image_forms = [
        (character, CharacterImageUploadForm(instance=character))
        for character in created_characters
    ]

    # Initialize other forms
    character_form = CharacterForm()
    campaign_form = CampaignForm()
    token_form = AccessTokenForm()
    token_form.fields['character'].queryset = created_characters

    if request.method == "POST":
        if 'create_character' in request.POST:  # Create a new character
            character_form = CharacterForm(request.POST)
            if character_form.is_valid():
                new_character = character_form.save(commit=False)
                new_character.save()
                new_character.profiles.add(profile)  # Associate with the user's profile
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

        #ChatGPT helped with this feature
        elif 'upload_image' in request.POST:  # Handle image upload
            character_id = request.POST.get('character_id')
            character = get_object_or_404(Character, id=character_id, profiles=profile)
            form = CharacterImageUploadForm(request.POST, request.FILES, instance=character)
            if form.is_valid():
                form.save()  # Save the uploaded image
                messages.success(request, f"Image uploaded for character '{character.name}'.")
            else:
                messages.error(request, f"Failed to upload image: {form.errors}")
            return redirect('user_dashboard')

        elif 'delete_image' in request.POST:  # Handle image deletion
            character_id = request.POST.get('character_id')
            character = get_object_or_404(Character, id=character_id, profiles=profile)
            if character.image:
                character.image.delete()  # Delete the image file
                character.image = None
                character.save()
                messages.success(request, f"Image deleted for character '{character.name}'.")
            else:
                messages.info(request, f"No image to delete for character '{character.name}'.")
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
        'character_image_forms': character_image_forms,  
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
