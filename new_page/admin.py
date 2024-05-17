from django.contrib import admin

from .models import Kullanici, Kupon, Post

for model in [Kullanici, Kupon, Post]:
    admin.site.register(model)
