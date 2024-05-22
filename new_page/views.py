# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, get_user_model, password_validation, hashers
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext_lazy as tercuman
from django.shortcuts import render, redirect
from new_page.models import Coach

User = get_user_model()

def LoginCall(request: HttpRequest):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        kullanici = authenticate(request, username=username, password=password)

        if kullanici is not None:
            login(request, kullanici)
            if kullanici.is_staff:
                return JsonResponse({'success': True, 'redirect_url': '/moderator'})

            else:
                return JsonResponse({'success': True, 'redirect_url': ''})

        else:
            return JsonResponse({'success': False, 'error': 'Yanlış Kullanıcı adı veya şifre'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'},status=400)

def RegisterCall(request: HttpRequest):
    if request.method == 'POST':
        username=request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Kullanıcı adı çoktan alınmış'})

        password=request.POST.get('password')
        password2= request.POST.get('confirm-password')
        if password != password2:
            return JsonResponse({'success': False, 'error': 'Parolalar aynı değil'})

        try:
            password_validation.validate_password(password)
            
            user = User.objects.create(username= username, password=hashers.make_password(password),
            first_name=request.POST.get('first-name'), last_name=request.POST.get('last-name'), email=request.POST.get('email'))
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': ''})

        except ValidationError as e:
            error_messages = [tercuman(message) + '\n' for message in e.messages]
            return JsonResponse({'success': False, 'error': error_messages})

def ModCall(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return render(request, 'admin.html', {'user': user})

        else:
            messages.error(request, 'Sen Moderator Değilsin!')
            return redirect('homepage')

    else:
            messages.error(request, 'Giriş yapmamışsın!')
            return redirect('homepage')

def CoachCall(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        try:
            coach_instance = Coach.objects.get(Kullanici=user)

            return render(request, 'post.html', {'user': user})

        except Coach.DoesNotExist:
            messages.error(request, 'Sen Koç Değilsin!')
            return redirect('homepage')
            
    else:
            messages.error(request, 'Giriş yapmamışsın!')
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
