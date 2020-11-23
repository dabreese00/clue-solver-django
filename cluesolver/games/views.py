from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.generic import ListView
from django.contrib import messages
from .models import Game, Player, GameCard, ClueRelation
from .forms import ClueRelationForm, CreateGameForm, PlayerForm


class HomeView(ListView):
    model = Game
    template_name = 'games/home.html'


def clone_card_to_gamecard(card, game):
    return GameCard.objects.create(
        name=card.name,
        card_type=card.card_type,
        game=game
    )


def create_game(request):

    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game = Game.objects.create()

            # from cards.models - Card, CardSet
            cardset = form.cleaned_data['card_set']
            for card in cardset.cards.all():
                _ = clone_card_to_gamecard(card, game)

            messages.success(
                request,
                'Game {} created.'.format(game.id)
            )
            return redirect('games:gameplay-dashboard', game.id)
    else:
        form = CreateGameForm()

    context = {'form': form}
    return render(request, 'games/create_game.html', context)


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
            return redirect('games:gameplay-dashboard', game.id)
        else:
            return HttpResponseBadRequest('Invalid form data.')

    form = ClueRelationForm()
    form.fields['player'].queryset = Player.objects.filter(game=game)
    form.fields['cards'].queryset = GameCard.objects.filter(game=game)

    context = {
        'game': game,
        'form': form
    }
    return render(request, 'games/gameplay_dashboard.html', context)


def create_player(request, game_id):

    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            p = Player.objects.create(
                name=form.cleaned_data['name'],
                hand_size=form.cleaned_data['hand_size'],
                game=game
            )

            messages.success(request, 'Player {} created'.format(p))
            return redirect('games:gameplay-dashboard', game.id)
    else:
        form = PlayerForm()
        context = {
            'game': game,
            'form': form
        }
        return render(request, 'games/create_player.html', context)
