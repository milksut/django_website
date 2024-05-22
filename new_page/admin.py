from django.contrib import admin

from .models import Kullanici, Kupon, Post, Match, Coach

for model in [Kullanici, Kupon, Post, Match, Coach]:
    admin.site.register(model)