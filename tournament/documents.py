from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from tournament.models import Team, Player

@registry.register_document
class TeamsDocument(Document):
    class Index:
        name = 'teams'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Team
        fields = [
            'name',
        ]

class PlayersDocument(Document):
    class Index:
        name = 'players'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Player
        fields = [
            'name',
            'position',
        ]
