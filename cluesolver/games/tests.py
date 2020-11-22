from django.test import TestCase

from games.models import Game, Player, GameCard, ClueRelation

class ClueRelationModelTests(TestCase):

    def test_new_have(self):
        g = Game.objects.create()
        p = Player.objects.create(name="David", hand_size=3, game=g)
        c = GameCard.objects.create(name="Professor Plum", card_type=GameCard.CardType.PERSON, game=g)
        r = ClueRelation.RelationType.HAVE

        cr = ClueRelation.objects.create(rel_type=r, player=p, game=g)
        cr.cards.add(c)
