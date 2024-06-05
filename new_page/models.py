from django.db import models
from django.contrib.auth.models import AbstractUser

class Kullanici(AbstractUser):
    balance = models.FloatField(blank=True,null=False, default=0)

    @property
    def is_coach(self):
        return hasattr(self, 'coach')

class Kupon(models.Model):
    oran = models.FloatField()
    yatirialan = models.FloatField(default=1, null=False)
    kazanc = models.FloatField(default=1, null=False)
    kupon_sayisi = models.PositiveIntegerField(default=1, null=False)
    Match = models.JSONField(default=dict) # oynanan_maclar[mac_id] = [team, value, mac_name]
    Kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)

class Match(models.Model):
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    minumum_bet_amount = models.PositiveIntegerField(default =1)
    match_date = models.DateField()
    odds_team1 = models.FloatField()
    odds_draw = models.FloatField()
    odds_team2 = models.FloatField()
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team1} vs {self.team2} - {self.match_date}"

class Coach(models.Model):
    CoachLeague= models.CharField(("Lig Uzmanligi"), max_length=50)
    Coachİmage = models.ImageField((""),upload_to="static/pictures")
    Kullanici = models.OneToOneField(Kullanici, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Kullanici.username} - {self.CoachLeague}"


class Post(models.Model):
    text = models.TextField(("Yorum"), max_length=600)
    Coach = models.ForeignKey(Coach, on_delete=models.CASCADE, default=1)
    match_tag = models.ManyToManyField(Match)
    def __str__(self):
        return self.text[:50]

