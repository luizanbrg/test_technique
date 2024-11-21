from rest_framework import viewsets
from tournament.api import serializers
from rest_framework.response import Response
from rest_framework import status
from tournament import models


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()



class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlayerSerializer
    queryset = models.Player.objects.all()

class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MatchSerializer
    queryset = models.Match.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs) #la methode super encapsule la methode de validation de l'objet, qui est appelée automatiquement. toute la logique de création de l'objet est géré par la classe mère
        match = self.get_object()
        self.match_stats(match) #j'ai opté pour séparer les responsabilités, la logique de calcul des stats est dans une méthode à part est pas dans la méthode create
        return response


    #méthode créé au cas où un match soit créé avec des erreurs de score, comme ça on peut le mettre à jour
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        match = self.get_object()
        self.match_stats(match)
        return response

    #methode où on calcule les stats des équipes après un match
    def match_stats(self, match):
        team1 = match.team1
        team2 = match.team2

        #si les deux équipes sont différentes, on peut continuer
        team1.kills_marked += match.team1_goals #buts marqués par l'équipe 1
        team1.kills_received += match.team2_goals #buts soufferts par l'équipe 1
        team2.kills_marked += match.team2_goals #buts marqués par l'équipe 2
        team2.kills_received += match.team1_goals #buts soufferts par l'équipe 2

        if match.team1_goals > match.team2_goals:
            team1.points += 3
        elif match.team1_goals < match.team2_goals:
            team2.points += 3
        else:
            team1.points += 1
            team2.points += 1

        if team1 == team2:
            return Response({'error': 'This is not possible, a team has to play against another team'}, status=status.HTTP_400_BAD_REQUEST)

        team1.save()
        team2.save()




#j'ai opté pour pas initialiser une viewset de position car je n'ai pas besoin d'effectuer des opérations crud sur ce modèle, je l'ai juste utilisé pour la relation avec le modèle player
