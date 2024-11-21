from django.test import TestCase
from django.urls import reverse
from ..models import Team, Player, Position, Match
from django.core.exceptions import ValidationError
from rest_framework import status

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

#     ###TEST MODEL RELATION TEAM ET PLAYER###

    def test_player_count_limit(self):
        for i in range(10):
            Player.objects.create(name=f"Player {i}", position=self.position, team=self.team)
        #10 sinon l'exception est levée à chaque fois
        with self.assertRaises(ValidationError):
            player = Player(name="Player 11", position=self.position, team=self.team)
            player.full_clean()
            player.save()

    def test_player_belongs_to_team(self):
        self.assertEqual(self.player.team, self.team)

#     ###TESTS MODEL PLAYER###
    def test_create_player(self):
        self.assertEqual(self.player.name, "TeamPlayer")
        self.assertEqual(self.player.position, self.position)
        self.assertEqual(self.player.team, self.team)

    def test_player_api_endpoint(self):
        response = self.client.get(reverse('players'))
        self.assertEqual(response.status_code, 200)

class MatchTestCase(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name="Banana", city="San Francisco")
        self.team2 = Team.objects.create(name="Strawberry Fields", city="Forever")
        self.team3 = Team.objects.create(name="Taylor Swift", city="Disney")

    def test_match_uniqueness(self):
        match = Match.objects.create(team1=self.team1, team2=self.team2, team1_goals=2, team2_goals=1)
        with self.assertRaises(ValueError):
            match = Match(team1=self.team1, team2=self.team2)
            match.full_clean()
            match.save()

    def test_match_different_teams(self):
        match1 = Match.objects.create(team1=self.team1, team2=self.team2)
        match2 = Match.objects.create(team1=self.team2, team2=self.team3)

        self.assertEqual(Match.objects.count(), 2)

    def test_match_same_team(self):
        match = Match(team1=self.team1, team2=self.team1)
        with self.assertRaises(ValidationError):
            match.full_clean()

    def test_match_results(self):
        match = Match.objects.create(team1=self.team1, team2=self.team2, team1_goals=3, team2_goals=1)

        self.team1.refresh_from_db()
        self.team2.refresh_from_db()

        self.assertEqual(self.team1.points, 3)
        self.assertEqual(self.team2.points, 0)
        self.assertEqual(self.team1.kills_marked, 3)
        self.assertEqual(self.team1.kills_received, 1)
        self.assertEqual(self.team2.kills_marked, 1)
        self.assertEqual(self.team2.kills_received, 3)

    def test_draw_match(self):
        match = Match.objects.create(team1=self.team1, team2=self.team2, team1_goals=2, team2_goals=2)

        self.team1.refresh_from_db()
        self.team2.refresh_from_db()

        self.assertEqual(self.team1.points, 1)
        self.assertEqual(self.team2.points, 1)
        self.assertEqual(self.team1.kills_marked, 2)
        self.assertEqual(self.team1.kills_received, 2)
        self.assertEqual(self.team2.kills_marked, 2)
        self.assertEqual(self.team2.kills_received, 2)
