from django.shortcuts import render

# Index view for the home page when I render the initial page
def index(request):
    return render(request, 'index.html')