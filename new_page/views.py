# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "homepage.html"


class SecondPageView(TemplateView):
    template_name = "second_page.html"
