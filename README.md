# **Tournoi de Football - Documentation GitHub**

Bienvenue dans la documentation de **My Django App**, mon premier projet fait sur le framework Django, où j'ai également utilisé la bibliothèque Django Rest Framework (DRF). Cette application a été faite dans un cadre d'apprentissage, où tout les concepts ont été nouveaus pour moi et je disposais de seulement 3 jours pour tout faire. 🌐✨

Cette application a été développée dans un but éducatif, en utilisant des bonnes pratiques du développement Django et des outils associés pour mieux comprendre l'architecture d'un projet Django, ce qui s'est avéré pas si difficile pour moi grâce aux enormes ressemblances de ce framework à Ruby on Rails, que j'ai déjà eu le plaisir d'utiliser dans le passé. 🎮🐍

---

## 🎯 **Objectif**

L'objectif principal de cette application est de permettre aux utilisateurs de visualiser le ranking d'un tournoi de football fictif, rentrer des joueurs et leurs respectives positions et équipes et rentrer aussi des nouvelles équipes.

---

## 🛠️ **Installation et Pré-requis**

### Prérequis

- Python 3.8+ installé.
- Django 4.x+ installé.
- PostGreSQL 14 ou +
- Un environnement virtuel Python est recommandé.

### Installation

1. Clonez ce dépôt GitHub :
   
```bash
git clone https://github.com/luizanbrg/test_technique.git
cd test_technique
```

2. Créez un environnement virtuel et activez-le :

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

4. Appliquez les migrations pour configurer la base de données :

```bash
python manage.py migrate
```

5. Démarrez le serveur de développement :

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌟 **Fonctionnalités**

- **Ranking et système de points :** Les équipes sont affichées selon leur position dans le ranking, où l'équipe avec le plus de points apparaît en première place. Un critère de kills_marked, c'est-à-dire, buts marqués, est utilisé en cas d'égalité, l'équipe ayant le plus de buts passe devant l'autre dans ce cas.
- **Liste de players :** Les players sont affichés sur une liste et les utilisateurs peuvent rentrer un nouveau joueur dans la db et un menu déroulant permet de choisir entre les équipes enregistrées et les positions de joueur.
- **Liste de teams :** Comme pour les players, les équipes sont affichées sur une liste et les utilisateurs peuvent rentrer une nouvelle équipe.

### 🎨 **Graphismes (UI/UX)**

L'application est conçue pour offrir une interface propre et intuitive, et Bootstrap a été utilisé pour donner un peu de style.

---

## 📂 **Structure des Fichiers**

```bash
tech_test_project/
├── manage.py
├── requirements.txt
├── tournament/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── migrations/
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   ├── test_views.py│  
│   ├── api/
│   │   ├── serializers.py
│   │   ├── viewsets.py
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   ├── templates/
│       ├── base.html
│       ├── homepage.html
│       ├── navbar.html
│       ├── players.html
│       ├── ranking.html
│       └── teams.html

```

---

## 🧩 **Code en Détail**

### Modèles Django

#### 1. **Team**
Le modèle `Team` représente une équipe et contient les informations suivantes :  
- **name** : Un nom unique pour chaque équipe. *(max_length=50)*  
- **city** : La ville associée à l'équipe. *(max_length=50)*  
- **points** : Le total des points accumulés par l'équipe (défaut : 0).  
- **kills_received** : Le nombre total de "kills" reçus par l'équipe (défaut : 0).  
- **kills_marked** : Le nombre total de "kills" marqués par l'équipe (défaut : 0).  

Chaque équipe est identifiée par son nom dans les affichages (`__str__`).

```python
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    points = models.PositiveIntegerField(default=0)
    kills_received = models.PositiveIntegerField(default=0)
    kills_marked = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
```

---

#### 2. **Position**
Le modèle `Position` définit les rôles ou positions des joueurs (par exemple : attaquant, défenseur). Chaque position doit être unique.

```python
class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
```

---

#### 3. **Player**
Le modèle `Player` représente un joueur.  
- **name** : Nom complet du joueur.  
- **team** : L'équipe à laquelle le joueur appartient (relation `ForeignKey`).  
- **position** : La position occupée par le joueur dans l'équipe (relation `ForeignKey`).  

**Règles personnalisées :**
- Une équipe ne peut pas avoir plus de 11 joueurs.  
  - Cette règle est implémentée dans la méthode `clean`, où on vérifie que le nombre de joueurs d'une équipe ne dépasse pas la limite avant d'autoriser la sauvegarde.

```python
class Player(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)

    def clean(self):
        if self.team and self.team.player_set.count() >= 11:
            raise ValidationError('A team cannot have more than 11 players.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
```

---

#### 4. **Match**
Le modèle `Match` représente une rencontre entre deux équipes.  
- **team1** : La première équipe participant au match.  
- **team2** : La deuxième équipe.  
- **team1_goals** et **team2_goals** : Nombre de buts marqués par chaque équipe.  

**Règles personnalisées :**
1. Une équipe ne peut pas jouer contre elle-même. *(Méthode `clean`)*
2. Deux équipes ne peuvent pas s'affronter plus d'une fois dans la base de données, quelle que soit l'ordre de `team1` et `team2`. *(Implémenté dans la méthode `save`)*
3. Après chaque sauvegarde, les statistiques des équipes sont mises à jour via un appel à la méthode `match_stats`.

**Méthode `match_stats` :**  
La méthode appelle une fonction externe définie dans le fichier `viewsets` pour calculer et mettre à jour les statistiques des équipes en fonction des résultats du match.

```python
class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team2')
    team1_goals = models.PositiveIntegerField(default=0)
    team2_goals = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError("A team cannot play against itself")

    def save(self, *args, **kwargs):
        if Match.objects.filter(team1=self.team1, team2=self.team2).exists() or Match.objects.filter(team1=self.team2, team2=self.team1).exists():
            raise ValueError("Two teams can't play twice against each other")
        super().save(*args, **kwargs)
        self.match_stats()

    def match_stats(self):
        from tournament.api.viewsets import MatchViewSet
        match_viewset = MatchViewSet()
        match_viewset.match_stats(self)

    def __str__(self):
        return f"{self.team1.name} against {self.team2.name}"
```

---

### Points forts de l'implémentation :
1. **Validation personnalisée** : Les méthodes `clean` garantissent que les règles métier (comme les restrictions sur le nombre de joueurs ou les matchs uniques) sont respectées.
2. **Gestion des relations** : L'utilisation des relations `ForeignKey` facilite la navigation entre les équipes, les joueurs et les matchs.
3. **Modularité** : Les méthodes comme `match_stats` délèguent le calcul des statistiques à des modules externes pour une meilleure organisation du code.


---

### ViewSets Django Rest Framework (DRF)

Les **ViewSets** permettent de simplifier la gestion des endpoints REST en regroupant toutes les opérations CRUD pour un modèle donné.
#### 1. **TeamViewSet**
Le `TeamViewSet` gère les opérations CRUD sur le modèle `Team`.  

**Fonctionnalités :**
- Utilisation du sérialiseur `TeamSerializer` pour valider et structurer les données.  
- Le queryset retourne toutes les instances de `Team`.  

**Code :**
```python
class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeamSerializer
    queryset = models.Team.objects.all()

```
---

#### 2. **PlayerViewSet**
Le `PlayerViewSet` gère les opérations CRUD pour les joueurs.  

**Fonctionnalités :**
- Utilise le sérialiseur `PlayerSerializer` 
- Le queryset retourne tous les joueurs.  

**Code :**
```python
class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PlayerSerializer
    queryset = models.Player.objects.all()
```

---

#### 3. **MatchViewSet**
Le `MatchViewSet` gère les opérations CRUD pour les matchs et inclut une logique métier complexe.  

**Fonctionnalités supplémentaires :**
1. **`create`** :
   - Appelle la méthode de validation et création standard (`super().create`).  
   - Déclenche la mise à jour des statistiques des équipes via une méthode dédiée : `match_stats`.  
   - Cette séparation des responsabilités garantit une meilleure organisation du code.  

2. **`update`** :
   - Similaire à `create`, mais utilisée pour les mises à jour des matchs (par exemple, correction des scores).  
   - Met à jour les statistiques des équipes après modification.  

3. **`match_stats`** :
   - Calcule et met à jour les statistiques des deux équipes après un match.  
   - Les règles métier incluent :  
     - Mise à jour des buts marqués et reçus pour chaque équipe.  
     - Attribution des points en fonction des résultats (3 pour une victoire, 1 pour un match nul).  

**Code :**
```python
class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MatchSerializer
    queryset = models.Match.objects.all()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)  # Appelle la logique standard de création
        match = self.get_object()
        self.match_stats(match)  # Met à jour les statistiques des équipes après création
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)  # Appelle la logique standard de mise à jour
        match = self.get_object()
        self.match_stats(match)  # Met à jour les statistiques après modification
        return response

    def match_stats(self, match):
        team1 = match.team1
        team2 = match.team2

        # Mise à jour des kills (buts marqués et reçus)
        team1.kills_marked += match.team1_goals
        team1.kills_received += match.team2_goals
        team2.kills_marked += match.team2_goals
        team2.kills_received += match.team1_goals

        # Attribution des points en fonction des scores
        if match.team1_goals > match.team2_goals:
            team1.points += 3
        elif match.team1_goals < match.team2_goals:
            team2.points += 3
        else:
            team1.points += 1
            team2.points += 1

        # Validation : une équipe ne peut pas jouer contre elle-même
        if team1 == team2:
            return Response(
                {'error': 'This is not possible, a team has to play against another team'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Sauvegarde des mises à jour
        team1.save()
        team2.save()
```

---

### Points forts et décisions importantes :
1. **Séparation des responsabilités** :
   - La méthode `match_stats` est distincte des méthodes `create` et `update`. Cela rend le code plus lisible et facilement testable.

2. **Gestion des exceptions** :
   - Lors de la création ou mise à jour d'un match, les règles métier (comme deux équipes ne pouvant pas s'affronter plusieurs fois) sont automatiquement validées.

3. **Validation métier dans `MatchViewSet`** :
   - Les règles complexes, comme l'attribution de points ou la mise à jour des statistiques, sont centralisées dans le ViewSet.

4. **ViewSet simplifié pour `Position`** :
   - Le modèle `Position` n'a pas de ViewSet dédié, car il est principalement utilisé pour définir des relations avec les joueurs et ne nécessite pas d'opérations CRUD exposées via une API.

---

### **Structure des URLs dans Django**

Le fichier `urls.py` est utilisé pour router les requêtes entrantes vers les différentes vues ou viewsets de l'application. J'utilise à la fois des **viewsets DRF** et des vues Django classiques.

---

### **1. Configuration générale**

Le fichier commence par importer les modules nécessaires :  
- **`admin`** : pour l'interface d'administration.  
- **`include`** : pour inclure des routes externes comme celles du `router`.  
- **Viewsets** : pour connecter l'API REST.  
- **Vues Django** : pour des pages web traditionnelles comme `homepage`.  

---

### **2. Le routeur DRF**

J'utilise un **`DefaultRouter`** de Django REST Framework (DRF).  
- Ce routeur crée automatiquement des endpoints RESTful pour les ViewSets enregistrés.  
- Les endpoints générés incluent les opérations CRUD standard (`create`, `read`, `update`, `delete`).

**Code :**
```python
router = routers.DefaultRouter()

router.register(r'teams', TeamViewSet, basename='Teams')
router.register(r'players', PlayerViewSet, basename='Players')
router.register(r'matches', MatchViewSet, basename='Matches')
```

**Explications :**
- **`r'teams'`** : l'URL de base pour accéder aux équipes sera `/teams/`.  
- Les mêmes principes s'appliquent pour les joueurs (`players`) et les matchs (`matches`).  

---

### **3. Les URL patterns**

**Code :**
```python
urlpatterns = [
    path('admin/', admin.site.urls),  # Interface d'administration Django
    path('api/', include(router.urls)),  # Inclut toutes les routes générées pour la partie API du routeur DRF
    path('', views.homepage, name='homepage'),  # Vue pour la page d'accueil
    path('teams/', views.teams, name='teams'),  # Vue pour la page des équipes
    path('players/', views.players, name='players'),  # Vue pour la page des joueurs
    path('ranking/', views.ranking, name='ranking'),  # Vue pour afficher le classement
]
```

**Explications :**
1. **Interface d'administration** :
   - **`admin/`** : Chemin vers l'interface d'administration standard de Django.

2. **Endpoints RESTful** :
   - **`api/`** : Préfixe pour toutes les API générées via DRF. Les endpoints RESTful suivants sont accessibles :
     - `/api/teams/` : Liste des équipes ou création d'une nouvelle équipe.
     - `/api/players/` : Liste des joueurs ou ajout d'un joueur.
     - `/api/matches/` : Liste des matchs ou ajout d'un match.
 

3. **Pages web traditionnelles** :
   - **`''`** : Chemin pour la page d'accueil (appelant la vue `homepage`).  
   - **`teams/`** : Page affichant des informations sur les équipes via la vue `teams`.  
   - **`players/`** : Page listant les joueurs via la vue `players`.  
   - **`ranking/`** : Page affichant le classement des équipes (`ranking`).  

---

## ⚽️ **Comment Utiliser l'application)**

1. Démarrez l'application avec le serveur Django local.
2. Rendez-vous à l'adresse suivante dans votre navigateur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### **Création de contenu**

Les **forms** utilisés dans ce projet permettent de créer des formulaires Django basés sur les modèles existants.

---

### **Structure des formulaires**

Les formulaires sont définis à l’aide de `forms.ModelForm`, une classe qui simplifie la création de formulaires liés directement aux modèles de la base de données. Ces formulaires permettent de gérer les données utilisateur avec un minimum de code.

---

### **1. Formulaire pour les équipes (TeamForm)**

#### Définition

```python
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['id', 'points', 'kills_received', 'kills_marked']
        labels = {
            'name': 'Team Name',
            'city': 'City',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your coolest team name here'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city here'}),
        }
```

#### Explications

1. **Modèle lié** :
   - Le formulaire est lié au modèle `Team` grâce à l’attribut `model`.

2. **Champs inclus** :
   - Tous les champs du modèle sont inclus par défaut avec `fields = '__all__'`.
   - Certains champs sont exclus explicitement grâce à `exclude`, notamment :
     - **`id`** : foreign key, générée automatiquement.
     - **`points`** :
     - **`kills_received`** et **`kills_marked`** : champs calculés automatiquement après les matchs.

3. **Labels** :
   - Les étiquettes (`labels`) permettent de renommer les champs dans le formulaire pour les rendre plus compréhensibles. Exemple :
     - **`name`** → "Team Name".
     - **`city`** → "City".

4. **Widgets** :
   - Les widgets contrôlent l’apparence et le comportement des champs HTML générés.
   - Exemple pour le champ `name` :
     - Utilisation de **`forms.TextInput`** avec des classes CSS Bootstrap (`form-control`) pour un design plus soigné.
     - Ajout d’un **placeholder** pour guider dans le remplissage.

---

### **2. Formulaire pour les joueurs (PlayerForm)**

#### Définition

```python
class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__'
        exclude = ['id']
        labels = {
            'name': 'Player Full Name',
            'team': 'Team',
            'position': 'Position',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name of the player'}),
        }
```

#### Explications

1. **Modèle lié** :
   - Ce formulaire est lié au modèle `Player`.

2. **Champs inclus** :
   - Tous les champs du modèle sont inclus grâce à `fields = '__all__'`, à l'exception de :
     - **`id`** : foreign key générée automatiquement.

3. **Labels** :
   - Les étiquettes (`labels`) permettent de donner des noms explicites aux champs :
     - **`name`** → "Player Full Name".
     - **`team`** → "Team".
     - **`position`** → "Position".

4. **Widgets** :
   - Exemple pour le champ `name` :
     - Utilisation de **`forms.TextInput`** avec des classes Bootstrap.
     - Ajout d’un placeholder indiquant que l’utilisateur doit entrer le nom complet du joueur.

---

### **3. Bonnes pratiques utilisées**

- **Exclusion des champs non nécessaires** :  
  Les champs comme `id` (foreign key) ou ceux mis à jour automatiquement par le système (`points`, `kills_received`, `kills_marked`.) sont exclus pour éviter qu’ils ne soient modifiables par l’utilisateur.

---

### **Conclusion**

- Ces formulaires fournissent une base solide pour gérer les données utilisateur tout en offrant des interfaces conviviales grâce à l’intégration de Bootstrap et aux personnalisations appliquées. Leur structure flexible permet de les adapter facilement à des besoins spécifiques ou à d'autres modèles de l'application.
---

## 🔍 **À Améliorer**

- **Tests automatisés :** Certains tests peuvent être améliorés, notamment ceux liés aux serializers.
- **Personnalisation de l'interface utilisateur :** Ajouter un design plus détaillé.
- Finir l'implémentation d'**Elastic Search** pour permettre la recherche par noms d'équipes et de joueurs/positions. 
- Déploiement et dockerisation 

---

## 🏆 **Résultats d'Apprentissage**

- Apprentissage du framework Django, qui a été très enrichissante. Je compte continuer à me former sur ce framework, c'était agréable d'utiliser un framework avec une organisation intuitive tout comme que Ruby on Rails. 
- Utilisation de modèles, vues et templates pour construire une architecture MVC (Model-View-Controller).
- Développement d'une interface utilisateur simple et fonctionnelle.
- Un peu sur football car je ne savais pas ce que 'kills' signifiait. 😂
- Un peu de Docker et Elastic Search. J'ai créé un container sur Docker pour la première fois !

---

## 🤯 **Difficultés rencontrées**

- Comprendre le fonctionnement du framework, comprendre le système de routages du DRF
- Comprendre le rôle et l'application des serializers, décider quand une validation devrait être sur un serializer ou sur un modèle
- Comprendre la différence entre view et viewset
- Lire la doc sur les tests unitaires, il y a beaucoup d'information.

---

## 👩🏻‍💻 Méthodologie appliquée

- Même travaillant toute seule, j'ai opté pour m'organiser de la meilleure façon possible dû au temps court. J'ai commencé par dessiner ma table sur [Football Match](https://drawsql.app/teams/luizas/diagrams/football-match), ensuite, j'ai commencé à écrire mes premières tâches sur [Trello Football](https://trello.com/b/twvWXfGW/football-tournament) pour avoir un suivi d'où j'étais, en plus de cocher les cases avec les tâches sur le doc word qui a été fourni.
- J'ai également travaillé sur une branche à mon nom, pour éviter tout casser sur la branche main. Je faisais branche luiza > dev > main.
- J'ai regardé énormement de vidéos YouTube sur Django pour me guier, en plus de lire énormement de doc aussi.
- Avoir un cahier pour noter (oui, à la main), des concepts clés sur Django ou le DRF que je trouvais utile avoir.  


