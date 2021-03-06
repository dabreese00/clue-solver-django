# Generated by Django 3.1.3 on 2020-11-22 02:50

from django.db import migrations

# Custom migration to help create new non-null foreign key
#
# References:
#
#   https://coderbook.com/@marcus/add-new-non-null-foreign-key-to-existing-django-model/
#
#   https://docs.djangoproject.com/en/3.1/ref/migration-operations/#django.db.migrations.operations.RunPython


def create_games(apps, schema_editor):
    Player = apps.get_model('games', 'Player')
    Card = apps.get_model('games', 'Card')
    ClueRelation = apps.get_model('games', 'ClueRelation')
    Game = apps.get_model('games', 'Game')

    models_linked_to_game = [Player, Card, ClueRelation]

    for model in models_linked_to_game:
        for obj in model.objects.all():
            instance, _ = Game.objects.get_or_create(id=1)
            obj.game = instance
            obj.save()


def reverse_create_games(apps, schema_editor):
    Player = apps.get_model('games', 'Player')
    Card = apps.get_model('games', 'Card')
    ClueRelation = apps.get_model('games', 'ClueRelation')
    Game = apps.get_model('games', 'Game')

    models_linked_to_game = [Player, Card, ClueRelation]

    for model in models_linked_to_game:
        for obj in model.objects.all():
            obj.game = None 
            obj.save()
    
    Game.objects.get(id=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20201122_0250'),
    ]

    operations = [
        migrations.RunPython(create_games, reverse_create_games),
    ]
