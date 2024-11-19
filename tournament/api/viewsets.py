from rest_framework import viewsets
from tournament.api import serializers
from tournament import models


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()
