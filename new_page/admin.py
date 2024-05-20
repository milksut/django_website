from django.contrib import admin

from .models import Post,Match



from .models import Match

admin.site.register(Match)



from .models import Kullanici, Kupon, Post

for model in [Kullanici, Kupon, Post]:
    admin.site.register(model)
