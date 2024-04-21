# Create your views here.
from django.views.generic import TemplateView, ListView
from .models import Post


class HomePageView(TemplateView):
    template_name = "homepage.html"


#class SecondPageView(ListView):
#   model = Post
#   template_name = "second_page.html"
