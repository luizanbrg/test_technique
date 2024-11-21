from rest_framework import serializers
from ..models import Player, Team, Position, Match

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

    def validate(self, data):
        team = data.get('team')

        if team and team.player_set.count() >= 11:
            raise serializers.ValidationError('A team cannot have more than 11 players.')

        return data

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
