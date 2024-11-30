from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Index view for the home page when I render the initial page
def index(request):
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    context = {
        'num_visits': num_visits
    }
    return render(request, 'index.html', context=context)

# This will render the login.html page so user's can attempt to authenticate to the application
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            return redirect("user_dashboard")  # Redirect to the user's dashboard or another page
        else:
            return render(request, "login.html", {"error": "Invalid username or password."})
    
    return render(request, "login.html")

@login_required
def user_dashboard(request):
    return render(request, "dashboard.html")

def logout_view(request):
    logout(request)  # Log out the user
    return redirect("login")  # Redirect to login page

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
