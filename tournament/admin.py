from django.contrib import admin
from .models import Position, Player

# Register your models here.

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'team']
    list_filter = ['position']
