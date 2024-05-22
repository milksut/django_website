from django.contrib import admin

from .models import Kullanici, Kupon, Post,Match

for model in [Kullanici, Kupon, Post, Match]:
    admin.site.register(model)