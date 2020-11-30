from django.test import TestCase
from games.models import Game, Player, GameCard, ClueRelation


class GameModelTests(TestCase):

    def test_hand_sizes_dont_add_up(self):
        g = Game.objects.create()
        person = GameCard.CardType.PERSON
        weapon = GameCard.CardType.WEAPON
        room = GameCard.CardType.ROOM
        card_tuple_list = (
            ("a", person),
            ("b", person),
            ("c", person),
            ("d", person),
            ("e", weapon),
            ("f", weapon),
            ("g", weapon),
            ("h", weapon),
            ("i", weapon),
            ("j", room),
            ("k", room),
            ("l", room),
            ("m", room),
            ("n", room),
            ("o", room),
        )
        for c in card_tuple_list:
            GameCard.objects.create(
                name=c[0],
                card_type=c[1],
                game=g
            )

        player_tuple_list = (
            ("a", 3),
            ("b", 3),
            ("c", 3),
            ("d", 4),
        )
        for p in player_tuple_list:
            Player.objects.create(
                name=p[0],
                hand_size=p[1],
                game=g
            )

        self.assertFalse(g.hand_sizes_add_up)

    def test_hand_sizes_add_up(self):
        g = Game.objects.create()
        person = GameCard.CardType.PERSON
        weapon = GameCard.CardType.WEAPON
        room = GameCard.CardType.ROOM
        card_tuple_list = (
            ("a", person),
            ("b", person),
            ("c", person),
            ("d", person),
            ("e", weapon),
            ("f", weapon),
            ("g", weapon),
            ("h", weapon),
            ("i", weapon),
            ("j", room),
            ("k", room),
            ("l", room),
            ("m", room),
            ("n", room),
            ("o", room),
        )
        for c in card_tuple_list:
            GameCard.objects.create(
                name=c[0],
                card_type=c[1],
                game=g
            )

        player_tuple_list = (
            ("a", 3),
            ("b", 3),
            ("c", 3),
            ("d", 3),
        )
        for p in player_tuple_list:
            Player.objects.create(
                name=p[0],
                hand_size=p[1],
                game=g
            )

        self.assertTrue(g.hand_sizes_add_up)


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
