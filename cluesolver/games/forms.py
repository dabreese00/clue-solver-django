from django import forms
from django.core.exceptions import ValidationError
from .models import ClueRelation, Player
from cards.models import CardSet


class ClueRelationForm(forms.ModelForm):
    class Meta:
        model = ClueRelation
        fields = ['rel_type', 'player', 'cards']

    def clean(self):
        cleaned_data = super().clean()
        rel_type = cleaned_data.get('rel_type')
        cards = cleaned_data.get('cards')

        if cards:
            # Do nothing if cards is already invalid
            if (rel_type in (
                        ClueRelation.RelationType.HAVE,
                        ClueRelation.RelationType.PASS)):
                if len(cards.all()) != 1:
                    raise ValidationError(
                        "A Have or Pass must contain exactly 1 card.",
                        code='invalid-haveorpass-card-count'
                    )
            else:
                if len(cards.all()) != 3:
                    raise ValidationError(
                        "A Show must contain exactly 3 cards.",
                        code='invalid-show-card-count'
                    )
                if not ClueRelation.validate_show_card_types(cards.all()):
                    raise ValidationError(
                        "A Show must contain 1 card of each type "
                        "(person, weapon, room).",
                        code='invalid-show-card-types'
                    )


class CreateGameForm(forms.Form):
    card_set = forms.ModelChoiceField(queryset=CardSet.objects.all())


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'hand_size']
