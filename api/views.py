from django.contrib.auth.models import User, Group
from cards.models import Card, CardSet
from games.models import Game, Player, GameCard, ClueRelation
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import (UserSerializer, GroupSerializer, CardSerializer,
                             CardSetSerializer, GameSerializer,
                             PlayerSerializer, GameCardSerializer,
                             ClueRelationSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardSetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows card sets to be viewed or edited.
    """
    queryset = CardSet.objects.all()
    serializer_class = CardSetSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed or edited.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]


class GameCardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows game cards to be viewed or edited.
    """
    queryset = GameCard.objects.all()
    serializer_class = GameCardSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClueRelationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clue relations to be viewed or edited.
    """
    queryset = ClueRelation.objects.all()
    serializer_class = ClueRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
