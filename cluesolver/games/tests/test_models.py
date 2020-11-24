from django.test import TestCase
from games.models import Game, Player, GameCard, ClueRelation


class ClueRelationModelTests(TestCase):

    def test_new_have(self):
        g = Game.objects.create()
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )
        c = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        r = ClueRelation.RelationType.HAVE

        cr = ClueRelation.objects.create(rel_type=r, player=p, game=g)
        cr.cards.add(c)

    def test_validate_show_card_types(self):
        g = Game.objects.create()
        c1 = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        c2 = GameCard.objects.create(
            name="Miss Scarlet",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        c3 = GameCard.objects.create(
            name="Knife",
            card_type=GameCard.CardType.WEAPON,
            game=g
        )

        valid_show = ClueRelation.validate_show_card_types([c1, c2, c3])
        self.assertIs(valid_show, False)

    def test_validate_show_card_types_pass(self):
        g = Game.objects.create()
        c1 = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        c2 = GameCard.objects.create(
            name="Ballroom",
            card_type=GameCard.CardType.ROOM,
            game=g
        )
        c3 = GameCard.objects.create(
            name="Knife",
            card_type=GameCard.CardType.WEAPON,
            game=g
        )

        valid_show = ClueRelation.validate_show_card_types([c1, c2, c3])
        self.assertIs(valid_show, True)
