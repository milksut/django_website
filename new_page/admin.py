from django.contrib import admin

from .models import Post,Match

admin.site.register(Post)

from .models import Match

admin.site.register(Match)from django.contrib import admin

from .models import Kullanici, Kupon, Post

for model in [Kullanici, Kupon, Post]:
    admin.site.register(model)
