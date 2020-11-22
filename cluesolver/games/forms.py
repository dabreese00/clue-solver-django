from django import forms
from .models import ClueRelation

class ClueRelationForm(forms.ModelForm):
    class Meta:
        model = ClueRelation
        fields = ['rel_type', 'player', 'cards']
