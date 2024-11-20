
# # Create your views here.

from django.shortcuts import render
from .models import Team
from .models import Player
from .forms import TeamForm
from .forms import PlayerForm
from django.http import HttpResponseRedirect

def homepage(request):
    return render(request, 'homepage.html')


def teams(request):

    #logique du forms pour add une equipe
    submitted = False
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teams?submitted=True') #le but de cette ligne est de garder l'utilisateur dans la page des équipes après avoir ajouté une équipe, la page se refresh sur elle même
    else:
        form = TeamForm()
        if 'submitted' in request.GET:
            submitted = True
            #le but de ce code est de vérifier si l'utilisateur a le 'submitted' dans l'url, si oui, on change la valeur de submitted à True


    #lister toutes les equipes
    teams_list = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams_list, 'form': form, 'submitted': submitted}) #le submitted ici va passer la variable submitted à la page teams.html

def players(request):

    submitted = False
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/players?submitted=True')
    else:
        form = PlayerForm()
        if 'submitted' in request.GET:
            submitted = True

    players_list = Player.objects.all()
    return render(request, 'players.html', {'players': players_list, 'form': form, 'submitted': submitted})
