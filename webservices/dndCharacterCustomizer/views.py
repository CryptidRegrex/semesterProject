from django.shortcuts import render

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
    return render(request, 'login.html')