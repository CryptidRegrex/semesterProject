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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dndCharacterCustomizer.viewsets import CharacterViewSet
from dndCharacterCustomizer.viewsets import UserRegistrationViewSet
#Will obtain the api key necessary to make a call to create a user
from rest_framework.authtoken.views import obtain_auth_token
from dndCharacterCustomizer import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'characters', CharacterViewSet, basename='character')
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
# router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('dndCharacterCustomizer/', include('dndCharacterCustomizer.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='dndCharacterCustomizer/',
                                  permanent=True))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
