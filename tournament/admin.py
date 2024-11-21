from django.contrib import admin
from .models import Position, Player, Team, Match

# Register your models here.

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'team']
    list_filter = ['position']

@admin.register(Team)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city']

@admin.register(Match)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'team1_id', 'team2_id', 'team1_goals', 'team2_goals']
