from django.test import TestCase
from tournament.api.serializers import TeamSerializer, PlayerSerializer, PositionSerializer
from tournament.models import Team, Player, Position

class PlayerSerializerTestCase(TestCase):

    def setUp(self):
        self.team = Team.objects.create(name="Equipe A", city="Paris")
        self.position = Position.objects.create(name="Forward")
        self.player_json = {'name': 'PlayerJsonTest', 'team': self.team.id, 'position': self.position.id } #ici on met self.team.id car il s'agit d'un dictionnaire, on simule un payload json et celui-ci ne comprend pas les objet django, ce qui nous oblige à mettre l'id de l'objet team

        self.player = Player.objects.create(name="PlayerTest", team=self.team, position=self.position)

    def test_serializer_deserialization_valid(self):
        serializer = PlayerSerializer(data=self.player_json)
        self.assertTrue(serializer.is_valid())
        player_instance = serializer.save() #ici on créé une instance de joueur faite à partir du player_json

        self.assertEqual(player_instance.name, self.player_json['name'])
        self.assertEqual(player_instance.team.id, self.player_json['team'])
        self.assertEqual(player_instance.position.id, self.player_json['position'])

    def test_serializer_deserialization_invalid_team(self):
        invalid_player = {
            'name': 'Player Test',
            'team': 999,  #tester si on peut instancier un player avec une equipe inexistante
            'position': self.position.id,
        }
        serializer = PlayerSerializer(data=invalid_player)
        self.assertFalse(serializer.is_valid())
        self.assertIn('team', serializer.errors) ##si l'erreur vient ailleurs que du team, le test fail

    def test_serializer_deserialization_invalid_position(self):
        invalid_json = {
            'name': 'Player Test',
            'team': self.team.id,
            'position': 999,  #tester avec une position inexistante
        }
        serializer = PlayerSerializer(data=invalid_json)
        self.assertFalse(serializer.is_valid())
        self.assertIn('position', serializer.errors)

    # def test_max_players_in_team_validation(self):
    #     for i in range(11):
    #         Player.objects.create(name=f"Super player {i}", team=self.team, position=self.position)

    #     invalid_player_json= {
    #         'name': 'Player 12',
    #         'team': self.team.id,
    #         'position': self.position.id,
    #     }
    #     serializer = PlayerSerializer(data=invalid_player_json)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('non_field_errors', serializer.errors)

class TeamSerializerTestCase(TestCase):

    def setUp(self):
        self.team_json = {'name': 'TeamTest', 'city': 'Juan-les-Pins'}
        self.team = Team.objects.create(name="TeamTest", city="Juan-les-Pins")

    def test_serializer_deserialization_valid(self):
        serializer = TeamSerializer(data=self.team_json)
        self.assertTrue(serializer.is_valid())
        team_instance = serializer.save()

        self.assertEqual(team_instance.name, self.team_json['name'])
        self.assertEqual(team_instance.city, self.team_json['city'])

    # def test_serializer_deserialization_invalid(self):
    #     invalid_team_json = {'name': 'TeamTest2', 'city': 'Juan-les-Pins'}
    #     serializer = TeamSerializer(data=invalid_team_json)
    #     self.assertTrue(serializer.is_valid())
    #     self.assertIn('city', serializer.errors)
