# Create your views here.
from django.views.generic import TemplateView, ListView
from .models import Post


class HomePageView(TemplateView):
    template_name = "homepage.html"
