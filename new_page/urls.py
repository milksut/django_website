from django.urls import path
from .views import HomePageView, BahislerPageView, KoclarPageView,ReklamPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("bahisler", BahislerPageView.as_view(), name="bahisler"),
    path("koclar", KoclarPageView.as_view(), name="koclar"),
    path("gain_1M$.com", ReklamPageView.as_view(), name="the_reklam"),
    ]
