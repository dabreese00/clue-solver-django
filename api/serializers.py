from django.contrib.auth.models import User, Group
from cards.models import Card, CardSet
from games.models import Game, Player, GameCard, ClueRelation
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ['url', 'name', 'card_type']


class CardSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CardSet
        fields = ['url', 'name', 'cards']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['url', 'created_timestamp', 'players', 'cards',
                  'known_relations']


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['url', 'name', 'hand_size', 'game']


class GameCardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameCard
        fields = ['url', 'name', 'card_type', 'game']


class ClueRelationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClueRelation
        fields = ['url', 'rel_type', 'player', 'cards', 'game']
