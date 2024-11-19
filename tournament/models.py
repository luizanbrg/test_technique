from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=255)

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

    def __str__(self):
        return self.name
