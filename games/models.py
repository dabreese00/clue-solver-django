from django.db import models


class Game(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Game {}, created {}".format(self.id, self.created_timestamp)

    @property
    def hand_sizes_add_up(self):
        """Check if hand sizes are consistent with total number of cards"""

        num_cards_in_hands = 0
        for p in self.players.all():
            num_cards_in_hands += p.hand_size

        return num_cards_in_hands == len(self.cards.all()) - 3


class Player(models.Model):

    name = models.CharField(max_length=255)
    hand_size = models.IntegerField()
    game = models.ForeignKey(
            Game,
            on_delete=models.CASCADE,
            related_name='players')

    class Meta:
        unique_together = ['name', 'game']

    def __str__(self):
        return "Player: {} (hand size: {})".format(self.name, self.hand_size)


class GameCard(models.Model):

    class CardType(models.TextChoices):
        PERSON = 'P'
        WEAPON = 'W'
        ROOM = 'R'

    name = models.CharField(max_length=255)
    card_type = models.CharField(max_length=1, choices=CardType.choices)
    game = models.ForeignKey(
            Game,
            on_delete=models.CASCADE,
            related_name='cards')

    class Meta:
        unique_together = ['name', 'game']

    def __str__(self):
        # TODO: Make card_type display label
        return "{} Card: {}".format(self.card_type, self.name)


class ClueRelation(models.Model):

    class RelationType(models.TextChoices):
        HAVE = 'H'
        SHOW = 'S'
        PASS = 'P'

    rel_type = models.CharField(max_length=1, choices=RelationType.choices)
    player = models.ForeignKey(
            Player,
            on_delete=models.CASCADE,
            related_name='relations_containing')
    cards = models.ManyToManyField(
            GameCard,
            related_name='relations_containing')
    game = models.ForeignKey(
            Game,
            on_delete=models.CASCADE,
            related_name='known_relations')

    def __str__(self):
        return "{} {}: {}".format(
                self.player.name,
                self.get_rel_type_display(),
                [str(c) for c in list(self.cards.all())])

    def validate_show_card_types(cards_list):
        """Check that a set of cards have valid types to comprise a show."""

        if len(cards_list) != len(GameCard.CardType):
            # We don't validate this here; it should have been already
            # validated before calling.
            raise ValueError("The number of cards is wrong.")

        card_types_represented = set([c.card_type for c in cards_list])
        card_types_possible = set(GameCard.CardType)

        return card_types_represented == card_types_possible
