from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.generic import ListView
from .models import Game, Player, GameCard, ClueRelation
from .forms import ClueRelationForm


class HomeView(ListView):
    model = Game
    template_name = 'games/home.html'


def gameplay_dashboard(request, game_id):

    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = ClueRelationForm(request.POST)
        if form.is_valid():
            r = ClueRelation.objects.create(
                rel_type=form.cleaned_data['rel_type'],
                player=form.cleaned_data['player'],
                game=game
            )
            r.cards.set(form.cleaned_data['cards'])
        else:
            return HttpResponseBadRequest('Invalid form data.')

    context = { 
        'game': game,
        'form': ClueRelationForm()
    }
    return render(request, 'games/gameplay_dashboard.html', context)
