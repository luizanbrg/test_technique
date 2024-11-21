from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    points = models.PositiveIntegerField(default=0)
    kills_received = models.PositiveIntegerField(default=0)
    kills_marked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)

 #ici je vais ajouter la methode pour ne pas avoir des teams plus grandes que 11 joueurs, on doit la faire sur le modele de player car c'est sur player que la relation entre les deux modèles est établie
    def clean(self):
        if self.team and self.team.player_set.count() >= 11:
            raise ValidationError('A team cannot have more than 11 players.')
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team2')
    team1_goals = models.PositiveIntegerField(default=0)
    team2_goals = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if Match.objects.filter(team1=self.team1, team2=self.team2).exists() or Match.objects.filter(team1=self.team2, team2=self.team1).exists():
            raise ValueError("Two teams can't play twice against each other") #par les querysets, python ira chercher dans la db si cette combination d'equipes existe déjà, et ce dans les deux sens que ce soit team1 = equipeA versus team2 = equipeB ou team1 = equipeB versus team2 = equipeA
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team1.name} against {self.team2.name}"
