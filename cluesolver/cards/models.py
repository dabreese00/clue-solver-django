from django.db import models

class Card(models.Model):

    class CardType(models.TextChoices):
        PERSON = 'P'
        WEAPON = 'W'
        ROOM   = 'R'

    name = models.CharField(max_length=255, unique=True)
    card_type = models.CharField(max_length=1, choices=CardType.choices)

    def __str__(self):
        # TODO: Make card_type display label
        return "{} Card: {}".format(self.card_type, self.name)

class CardSet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    cards = models.ManyToManyField(Card)

    def __str__(self):
        return "Card Set: {}".format(self.name)
