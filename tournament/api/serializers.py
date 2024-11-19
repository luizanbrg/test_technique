from rest_framework import serializers
from tournament import models

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'
