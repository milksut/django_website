from django.db import models
from django.contrib.auth.models import AbstractUser

class Kullanici(AbstractUser):
    balance = models.FloatField(blank=True,null=False, default=0)

class Kupon(models.Model):
    oran = models.FloatField()
    Kullanici = models.ForeignKey(Kullanici, on_delete=models.CASCADE)

class Post(models.Model):
    text = models.TextField()

    def __str__(self):  # new
        return self.text[:50]
