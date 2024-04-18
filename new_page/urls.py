from django.urls import path
from .views import SecondPageView, HomePageView
urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("second", SecondPageView.as_view(), name="secondary")
    ]
