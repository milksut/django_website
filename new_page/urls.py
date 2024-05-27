from django.urls import path
from .views import HomePageCall, BahislerPageCall, KoclarPageCall, ReklamPageView, KuponCall, PostCall, contact_upload
from .views import IletisimPageView, LoginCall, RegisterCall, ModCall, CoachCall, LogoutCall, ResetPasswordCall

urlpatterns = [
    path("", HomePageCall, name="homepage"),
    path("bahisler", BahislerPageCall, name="bahisler"),
    path("koclar", KoclarPageCall, name="koclar"),
    path("gain_1M$.com", ReklamPageView.as_view(), name="the_reklam"),
    path("iletisim.com", IletisimPageView.as_view(), name="iletisim"),
    path('login', LoginCall, name='loginCall'),
    path('register', RegisterCall, name='registerCall'),
    path('moderator', ModCall, name='modCall'),
    path('contact', contact_upload, name='contact'),
    path('post', CoachCall, name='coachCall'),
    path('logout', LogoutCall, name='logoutCall'),
    path('kuponUpdate', KuponCall, name='kuponCall'),
    path('list_posts', PostCall, name='postCall'),
    path('reset_password', ResetPasswordCall, name='resetPasswordCall'),
    ]
