"""
URL configuration for webservices project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dndCharacterCustomizer import views
from django.conf import settings
from django.conf.urls.static import static
from dndCharacterCustomizer.views import index, login_view, user_dashboard, logout_view, register_view, update_character, update_account, reset_password_request, reset_password_confirm
#from rest_framework.routers import DefaultRouter
# from dndCharacterCustomizer.viewsets import CharacterViewSet
# from dndCharacterCustomizer.viewsets import UserRegistrationViewSet
#Will obtain the api key necessary to make a call to create a user
#from rest_framework.authtoken.views import obtain_auth_token
#from django.views.generic import TemplateView
#from django.views.generic import RedirectView


# router = DefaultRouter()
# router.register(r'characters', CharacterViewSet, basename='character')
# router.register(r'register', UserRegistrationViewSet, basename='user-registration')
# router.register(r'users', UserViewSet, basename='user')

#static was used for media creation this sets the media's default location from the settings.py
urlpatterns = [
    path('', index, name='index'),
    path('6151024e-d149-49f8-b40b-cbd19554ec40/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('character/<int:character_id>/update/', update_character, name='update_character'),
    path('character/<int:character_id>/', views.character_detail, name='character_detail'),
    path("account/update/", update_account, name="update_account"),
    path("reset-password/", reset_password_request, name="reset_password"),
    path("reset-password/<str:token>/", reset_password_confirm, name="reset_password_confirm"),
    #path('api', include(router.urls)),
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

