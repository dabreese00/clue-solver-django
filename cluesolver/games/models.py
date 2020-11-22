from django.db import models


class Game(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)


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
        ROOM   = 'R'

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
        # TODO: Generalize for relations with more than 1 card.
        # TODO: Make rel_type display label
        return "{} {}: [{}]".format(
                self.player, 
                self.rel_type, 
                self.cards.first())
