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
