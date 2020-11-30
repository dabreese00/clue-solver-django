from django.contrib import admin
from .models import Player, GameCard, ClueRelation, Game

admin.site.register(Player)
admin.site.register(GameCard)
admin.site.register(ClueRelation)
admin.site.register(Game)
