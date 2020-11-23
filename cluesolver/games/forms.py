from django import forms
from .models import ClueRelation, Player
from cards.models import CardSet


class ClueRelationForm(forms.ModelForm):
    class Meta:
        model = ClueRelation
        fields = ['rel_type', 'player', 'cards']


class CreateGameForm(forms.Form):
    card_set = forms.ModelChoiceField(queryset=CardSet.objects.all())


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'hand_size']
