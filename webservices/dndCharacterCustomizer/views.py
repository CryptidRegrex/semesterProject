from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Character, Campaign
#This took forever to figure out. Essentially we are going to call django's native login() function and we are going to rename it to make it clear what it is
#used within login_view definition
from django.contrib.auth import authenticate, login as auth_login

from .forms import CharacterForm, CampaignForm

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
@login_required
def user_dashboard(request):
    # Get the Profile of the logged-in user
    profile = Profile.objects.get(user=request.user)
    
    # Get all related Campaigns and Characters
    campaigns = profile.campaigns.all()
    characters = profile.owners.all() 

    # Check if no campaigns or characters exist and set fallback messages
    campaigns_message = "No Campaigns" if not campaigns else None
    characters_message = "No Characters" if not characters else None
    
    # Handle creating a new Character
    if request.method == "POST":
        if 'create_character' in request.POST:
            character_form = CharacterForm(request.POST)
            if character_form.is_valid():
                new_character = character_form.save(commit=False)
                new_character.save()  # Save the character to postgresql
                
                # Associate the new character with the logged-in user
                new_character.profiles.add(profile)
                return redirect('user_dashboard')  # Redirect to the dashboard after saving
        elif 'create_campaign' in request.POST:
            campaign_form = CampaignForm(request.POST)
            if campaign_form.is_valid():
                new_campaign = campaign_form.save(commit=False)
                new_campaign.save()  # Save the campaign to postgresql
                
                # Associate the new campaign with the logged-in user
                new_campaign.profiles.add(profile)
                return redirect('user_dashboard')  # Redirect to the dashboard after saving

    # Forms to create new characters and campaigns
    character_form = CharacterForm()
    campaign_form = CampaignForm()

    # Pass the context information to the templates
    context = {
        'profile': profile,
        'campaigns': campaigns,
        'characters': characters,
        'character_form': character_form,
        'campaign_form': campaign_form
    }
    return render(request, 'dashboard.html', context)


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
