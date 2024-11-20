from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)

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
