# Create your views here.
from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password

def LoginCall(request: HttpRequest):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        kullanici = authenticate(request, username=username, password=password) 
        print(username,password)
        if kullanici is not None:
            login(request, kullanici)
        else:
            return redirect('koclar')
    return redirect('homepage')

class HomePageView(TemplateView):
    template_name = "homepage.html"

class BahislerPageView(TemplateView):
    template_name = "bahisler.html"

class KoclarPageView(TemplateView):
    template_name = "koclar.html"

class ReklamPageView(TemplateView):
    template_name = "the_big_add.html"

class IletisimPageView(TemplateView):
    template_name = "iletisim.html"
