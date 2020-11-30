import unittest
from django.test import TestCase, Client
from django.urls import reverse
from games.models import Game, Player, GameCard


class GameplayDashboardViewTests(TestCase):

    def test_invalid_show_wrong_types(self):
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
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )
        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'S',
                                   'player': p.id,
                                   'cards': [c1.id, c2.id, c3.id]
                               })
        form = response.context['form']

        self.assertTrue(
            form.has_error(
                '__all__',  # __all__ is the "field name" for non-field errors
                code='invalid-show-card-types'
            )
        )

    def test_valid_show_right_types(self):
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
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )
        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'S',
                                   'player': p.id,
                                   'cards': [c1.id, c2.id, c3.id]
                               })
        self.assertEqual(response.status_code, 302)

    def test_invalid_show_wrong_number_cards(self):
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
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )

        # Extra data to catch other games bleeding into form
        g2 = Game.objects.create()
        _ = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g2
        )
        _ = GameCard.objects.create(
            name="Miss Scarlet",
            card_type=GameCard.CardType.PERSON,
            game=g2
        )

        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'S',
                                   'player': p.id,
                                   'cards': [c1.id, c2.id]
                               })
        form = response.context['form']

        self.assertTrue(
            form.has_error(
                '__all__',  # __all__ is the "field name" for non-field errors
                code='invalid-show-card-count'
            )
        )

        # Catch other games bleeding into form
        for fieldname in ['player', 'cards']:
            field = form.fields[fieldname]
            for q in field.queryset:
                with self.subTest(i=q):
                    self.assertEqual(q.game, g)

    def test_invalid_have_wrong_number_cards(self):
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
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )
        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'H',
                                   'player': p.id,
                                   'cards': [c1.id, c2.id]
                               })
        form = response.context['form']

        self.assertTrue(
            form.has_error(
                '__all__',  # __all__ is the "field name" for non-field errors
                code='invalid-haveorpass-card-count'
            )
        )

    def test_valid_have(self):
        g = Game.objects.create()
        c1 = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )
        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'H',
                                   'player': p.id,
                                   'cards': c1.id
                               })

        self.assertEqual(response.status_code, 302)

    def test_valid_pass(self):
        g = Game.objects.create()
        c1 = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g
        )
        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'P',
                                   'player': p.id,
                                   'cards': c1.id
                               })

        self.assertEqual(response.status_code, 302)

    @unittest.skip("not implemented yet")
    def test_invalid_pass_discrepant_game(self):
        g = Game.objects.create()
        g2 = Game.objects.create()
        c1 = GameCard.objects.create(
            name="Professor Plum",
            card_type=GameCard.CardType.PERSON,
            game=g
        )
        p = Player.objects.create(
            name="David",
            hand_size=3,
            game=g2
        )
        client = Client()
        response = client.post(reverse('games:gameplay-dashboard', args='1'),
                               {
                                   'rel_type': 'P',
                                   'player': p.id,
                                   'cards': c1.id
                               })

        self.assertNotEqual(response.status_code, 302)

    def test_invalid_player_hand_size(self):
        g = Game.objects.create()
        cards = set()
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
            cards.add(GameCard.objects.create(
                name=c[0],
                card_type=c[1],
                game=g
            ))

        players = set()
        player_tuple_list = (
            ("a", 3),
            ("b", 3),
            ("c", 3),
        )
        for p in player_tuple_list:
            players.add(Player.objects.create(
                name=p[0],
                hand_size=p[1],
                game=g
            ))

        # Upon adding player "d", players collectively have 13 cards, leaving
        # only 2 for the confidential file.
        client = Client()

        # Form submission should succeed
        response = client.post(reverse('games:create-player', args='1'),
                               {
                                   'name': 'd',
                                   'hand_size': 4
                               })

        self.assertEqual(
            response.status_code,
            302
        )

        # But the dashboard template should be aware of the mismatch
        response = client.get(reverse('games:gameplay-dashboard', args='1'))

        self.assertFalse(response.context['game'].hand_sizes_add_up)

    def test_valid_player_hand_size(self):
        g = Game.objects.create()
        cards = set()
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
            cards.add(GameCard.objects.create(
                name=c[0],
                card_type=c[1],
                game=g
            ))

        players = set()
        player_tuple_list = (
            ("a", 3),
            ("b", 3),
            ("c", 3),
        )
        for p in player_tuple_list:
            players.add(Player.objects.create(
                name=p[0],
                hand_size=p[1],
                game=g
            ))

        client = Client()

        # Form submission should succeed
        response = client.post(reverse('games:create-player', args='1'),
                               {
                                   'name': 'd',
                                   'hand_size': 3
                               })

        self.assertEqual(
            response.status_code,
            302
        )

        response = client.get(reverse('games:gameplay-dashboard', args='1'))

        self.assertTrue(response.context['game'].hand_sizes_add_up)
