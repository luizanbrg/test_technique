
# # Create your views here.

from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def teams(request):
    return render(request, 'teams.html')
