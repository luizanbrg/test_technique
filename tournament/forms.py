from django import forms
from django.forms import ModelForm
from .models import Team
from .models import Player

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['id', 'points', 'kills_received', 'kills_marked']

        labels = {
            'name': 'Team Name',
            'city': 'City',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your coolest team name here'}), #le form-control hash permet de bootstraper le forms pour un peu de design
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city here'}),
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['id']

        labels = {
            'name': 'Player Full Name',
            'team': 'Team',
            'position': 'Position',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name of the player'}),
        }
