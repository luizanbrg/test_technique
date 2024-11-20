from django.test import TestCase
from django.urls import reverse
from ..models import Team, Player, Position
from django.core.exceptions import ValidationError

# Create your tests here.

#tester un model

class ModelTestCase(TestCase):

    def setUp(self):
        self.team = Team.objects.create(name="TeamTest", city="Nice")
        self.position = Position.objects.create(name="Forward")
        self.player = Player.objects.create(name="TeamPlayer", position=self.position, team=self.team)

    ###ICI TESTS TEAM MODEL###
    def test_team_creation(self):
        self.assertEqual(self.team.name, "TeamTest")

    def test_team_api_endpoint(self):
        response = self.client.get(reverse('teams'))
        self.assertEqual(response.status_code, 200)

    ###TEST MODEL RELATION TEAM ET PLAYER###

    def test_player_count_limit(self):
        for i in range(10):
            Player.objects.create(name=f"Player {i}", position=self.position, team=self.team)
        #10 sinon l'exception est levée à chaque fois
        with self.assertRaises(ValidationError):
            player = Player(name="Player 11", position=self.position, team=self.team)
            player.save()

    def test_player_belongs_to_team(self):
        self.assertEqual(self.player.team, self.team )

    ###TESTS MODEL PLAYER###
    def test_create_player(self):
        self.assertEqual(self.player.name, "TeamPlayer")
        self.assertEqual(self.player.position, self.position)
        self.assertEqual(self.player.team, self.team)

    def test_player_api_endpoint(self):
        response = self.client.get(reverse('players'))
        self.assertEqual(response.status_code, 200)
