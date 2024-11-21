"""
URL configuration for tech_test_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from tournament.api import viewsets as teamsviewsets
from tournament.api import viewsets as playersviewsets
from tournament.api import viewsets as matchesviewsets

from rest_framework import routers

from tournament import views

router = routers.DefaultRouter()

router.register(r'teams', teamsviewsets.TeamViewSet, basename='Teams')
router.register(r'players', playersviewsets.PlayerViewSet, basename='Players')
router.register(r'matches', matchesviewsets.MatchViewSet, basename='Matches')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.homepage, name='homepage'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('ranking/', views.ranking, name='ranking'),
]
