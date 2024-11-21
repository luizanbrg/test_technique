from django.test import TestCase
from django.urls import reverse
from tournament.models import Team

class RankingViewTestCase(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name="Orangina", city="Orangigi", points=5, kills_marked=10)
        self.team2 = Team.objects.create(name="Coca Cola", city="Cocaca", points=3, kills_marked=8)
        self.team3 = Team.objects.create(name="Sprite", city="Spripi", points=5, kills_marked=15)

    def test_ranking_view(self):
        response = self.client.get(reverse('ranking')) #appeler la vue ranking
        self.assertEqual(response.status_code, 200)

        teams = response.context['teams']
        self.assertEqual(teams[0].name, "Sprite") #la première doit être Sprite car elle a plus de kils marked
        self.assertEqual(teams[1].name, "Orangina")
        self.assertEqual(teams[2].name, "Coca Cola")
