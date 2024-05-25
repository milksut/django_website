# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model, password_validation, hashers
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext_lazy as tercuman
from django.shortcuts import render, redirect
from new_page.models import Coach, Match, Kupon, Post

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

            elif kullanici.is_coach:
                return JsonResponse({'success': True, 'redirect_url': '/post'})

            else:
                return JsonResponse({'success': True, 'redirect_url': ''})

        else:
            return JsonResponse({'success': False, 'error': 'Yanlış Kullanıcı adı veya şifre'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'},status=400)

def RegisterCall(request: HttpRequest):
    if request.method == 'POST':
        username=request.POST.get('register-username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Kullanıcı adı çoktan alınmış'})

        password=request.POST.get('register-password')
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
        if user.is_coach:
            return render(request, 'post.html', {'user': user})

        else:
            messages.error(request, 'Sen Koç Değilsin!')
            return redirect('homepage')
            
    else:
            messages.error(request, 'Giriş yapmamışsın!')
            return redirect('homepage')

def LogoutCall(request):
    logout(request)
    return redirect('homepage')

def HomePageCall(request):
    Coachs = Coach.objects.filter(is_featured=True)
    matches = Match.objects.filter(is_featured=True)
    return render(request, 'homepage.html', {'Coachs': Coachs, 'matches':matches})

def BahislerPageCall(request):
    matches = Match.objects.all()
    return render(request, 'bahisler.html', {'matches': matches})

def KoclarPageCall(request):
    Coachs = Coach.objects.all()
    return render(request, 'koclar.html', {'Coachs': Coachs})

class ReklamPageView(TemplateView):
    template_name = "the_big_add.html"

class IletisimPageView(TemplateView):
    template_name = "iletisim.html"

def KuponCall(request: HttpRequest):
    if request.method == 'POST':
        if request.user.is_authenticated:
            tutar = float(request.POST.get('Tutar'))
            if tutar <= int(request.user.balance):
                oran = float(request.POST.get('send-oran'))
                kazanc = float(request.POST.get('send-kazanc'))
                amount = int(request.POST.get('Sayi'))
                maclar_json = request.POST.get('send-dict')
                Kupon.objects.create(oran=oran, yatirialan=tutar ,kazanc=kazanc, kupon_sayisi=amount, Kullanici=request.user, Match=maclar_json)
                request.user.balance -= tutar
                request.user.save()
                return redirect('koclar')

            else:
                messages.error(request, 'Bu kupon için yeterli bakiyen yok !')
                return redirect('homepage')
        else:
            messages.error(request, 'Giriş yapmadan kupon oynayamassın!')
            return redirect('homepage')
    else:
        messages.error(request, 'Geçersiz Method')
        return redirect('homepage')

def PostCall(request: HttpRequest):
    if request.method == "GET":
        Posts = Post.objects.all()
        coach = request.GET.get('Coach')
        match_tag = request.GET.get('match_tag')
        print(coach, match_tag)
        if request.GET:
            if coach:
                Posts = Posts.filter(Coach_id=coach)
            if match_tag:
                Posts = Posts.filter(match_tag__id=match_tag)

        match_tags = Match.objects.filter(post__in=Posts).distinct()
        return render(request, 'posts.html', {'posts' : Posts, 'match_tags': match_tags, 'coach':coach})
    else:
        messages.error(request, 'Geçersiz Method')
        return redirect('homepage')
