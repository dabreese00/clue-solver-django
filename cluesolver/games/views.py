from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Game

#def home(request):
#    return render(request, 'home.html', {})

class HomeView(ListView):
    model = Game
    template_name = 'games/home.html'

class GameplayDashboardView(DetailView):
    model = Game
    template_name = 'games/gameplay_dashboard.html'
