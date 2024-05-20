from django.db import models

# models.py
from django.db import models

class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    match_date = models.DateField()
    odds_team1 = models.FloatField()
    odds_draw = models.FloatField()
    odds_team2 = models.FloatField()

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.match_date}"



class Post(models.Model):
    text = models.TextField()

    def __str__(self):  # new
        return self.text[:50]
