# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext_lazy as tercuman

User = get_user_model()

def LoginCall(request: HttpRequest):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        kullanici = authenticate(request, username=username, password=password) 
        if kullanici is not None:
            login(request, kullanici)
            if username == "admin":
                return JsonResponse({'success': True, 'redirect_url': '/admin'})
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
        password2= request.POST.get('password2')
        if password != password2:
            return JsonResponse({'success': False, 'error': 'Parolalar aynı değil'})
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            error_messages = [tercuman(message) for message in e.messages]
            return JsonResponse({'success': False, 'error': error_messages})
        user = User.objects.create(username= username, password=password, first_name=request.POST.get('first_name'),
            lasr_name=request.POST.get('last_name'), email=request.POST.get('email'))
        login(request, user)
        return JsonResponse({'success': True})


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
