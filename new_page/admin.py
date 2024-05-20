from django.contrib import admin

from .models import Post,Match

admin.site.register(Post)

from .models import Match

admin.site.register(Match)