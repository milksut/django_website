# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model, password_validation, hashers
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.translation import gettext_lazy as tercuman
import csv, io
from django.contrib.auth.decorators import  permission_required
from django.shortcuts import render, redirect, get_object_or_404
from new_page.models import Coach, Match, Kupon, Post
from django.db.models import Q
from datetime import datetime

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
                messages.success(request, 'Hoşgeldin '+username+"!")
                return JsonResponse({'success': True, 'redirect_url': '/'})

        else:
            return JsonResponse({'success': False, 'error': 'Yanlış Kullanıcı adı veya şifre'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'},status=405)

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
            messages.success(request, 'Kayıt Olma Başarılı!')
            return JsonResponse({'success': True, 'redirect_url': '/'})

        except ValidationError as e:
            error_messages = [tercuman(message) + '\n' for message in e.messages]
            return JsonResponse({'success': False, 'error': error_messages})

def ResetPasswordCall(request: HttpRequest):
    if request.method == 'POST':
        new_password=request.POST.get('reset-new-password')
        confrim_password=request.POST.get('reset-confrim-password')
        old_password=request.POST.get('reset-old-password')

        if new_password != confrim_password:
            return JsonResponse({'success': False, 'error': ' Yeni parolalar aynı değil!'})

        if not request.user.check_password(old_password):
            return JsonResponse({'success': False, 'error': 'Eski parola aynı değil!'})
        
        if new_password == old_password:
            return JsonResponse({'success': False, 'error': 'Eski parola ve yeni parola aynı olamaz!'})
        
        try:
            password_validation.validate_password(new_password)

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Şifre Başarıyla değiştirildi!')
            return JsonResponse({'success': True, 'redirect_url': '/'})

        except ValidationError as e:
            error_messages = [tercuman(message) + '\n' for message in e.messages]
            return JsonResponse({'success': False, 'error': error_messages})

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'},status=405)

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
    if request.method == "GET":
        if user.is_authenticated:
            if user.is_coach:
                matches = Match.objects.all()
                return render(request, 'post.html', {'user': user, "match_tags":matches})

            else:
                messages.error(request, 'Sen Koç Değilsin!')
                return redirect('homepage')
                
        else:
            messages.error(request, 'Giriş yapmamışsın!')
            return redirect('homepage')
    
    elif request.method == "POST":
        if user.is_authenticated:
            if user.is_coach:
                text = request.POST.get('post_text')
                match_tags = request.POST.getlist('match_tag_select')

                post = Post.objects.create(Coach=user.coach, text=text)

                for match_id in match_tags:
                    match = Match.objects.get(id=match_id)
                    post.match_tag.add(match)

                post.save()

                messages.success(request, 'Post Kaydedildi !')
                return redirect('coachCall')
            else:
                messages.error(request, 'Sen Koç Değilsin!')
                return redirect('homepage')
        else:
            messages.error(request, 'Giriş yapmamışsın!')
            return redirect('homepage')

    else:
        messages.error(request, 'Geçersiz Method')
        return redirect('homepage')

def LogoutCall(request):
    logout(request)
    return redirect('homepage')

def HomePageCall(request):
    Coachs = Coach.objects.filter(is_featured=True)
    matches = Match.objects.filter(is_featured=True)
    return render(request, 'homepage.html', {'Coachs': Coachs, 'matches':matches})

def BahislerPageCall(request):
    if request.method == "GET":
        name = request.GET.get('name')
        matches = Match.objects.all()
        if name:
            matches = matches.filter(Q(team1__icontains=name) | Q(team2__icontains=name))
        return render(request, 'bahisler.html', {'matches': matches})

def KoclarPageCall(request):
    Coachs = Coach.objects.all()
    return render(request, 'koclar.html', {'Coachs': Coachs})

class ReklamPageView(TemplateView):
    template_name = "the_big_add.html"

class IletisimPageView(TemplateView):
    template_name = "iletisim.html"

@permission_required('admin.can_add_log_entry')
def contact_upload(request):
    template = "admin.html"
    
    print("aaaaaaaaaaaaaaaaa")
    print(request.method)
    print("aaaaaaaaaaaaaaaaa")
    if request.method == "GET":
        response = HttpResponse(content_type='text/csv')
        content = request.GET.get('content')
        response['Content-Disposition'] = 'attachment; filename=' + content + ".csv"
        writer = csv.writer(response)

        if content == "mac":
            writer.writerow(["team1", "team2", "minumum_bet_amount", "match_date", "odds_team1",
            "odds_draw", "odds_team2", "is_featured", "id"])

            for mac in Match.objects.all():
                writer.writerow([mac.team1, mac.team2, mac.minumum_bet_amount, mac.match_date,
                mac.odds_team1, mac.odds_draw, mac.odds_team2, mac.is_featured, mac.id])
            
            return response

        elif content == "post":
            writer.writerow(["text", "Coach", "Coach_id", "post_id", "match_tag", "tag_names"])

            for post in Post.objects.all():
                match_tags = post.match_tag.all()
                compiled_tag_names = ", ".join([mac.team1 + " vs " + mac.team2 for mac in match_tags])
                compiled_tag_ids = ", ".join([str(mac.id) for mac in match_tags])
                writer.writerow([post.text, post.Coach, post.Coach.id, post.id, compiled_tag_ids, compiled_tag_names])
            
            return response
        
        else:
            messages.error(request, "Böyle bir export yok!")
            return render(request, template)
    
    elif request.method == "POST":
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Sadice csv dosyası kabul edilir!")
            return render(request, template)
        
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        content = request.POST.get('content')

        if content == "mac":
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                try:
                    Match.objects.update_or_create(
                        team1 = column[0].strip(),
                        team2 = column[1].strip(),
                        minumum_bet_amount = int(column[2].strip()),
                        match_date = datetime.strptime(column[3].strip(), '%Y-%m-%d').date(),
                        odds_team1 = float(column[4].strip()),
                        odds_draw = float(column[5].strip()),
                        odds_team2 = float(column[6].strip()),
                        is_featured = column[7].strip().lower() == 'true',
                        id = int(column[8].strip())
                    )

                except ValueError as e:
                    messages.error(request, f"{column} Satırını İşlerken Bir Hata Meydana Geldi: {e}")
                    return render(request, template)

            messages.success(request, "Maclar csv dosyası başarıyla yüklendi")
            return render(request, template)

        elif content == "post":
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                try:
                    match_ids = [int(id.strip()) for id in column[4].split(',')]
                    post, created = Post.objects.update_or_create(
                        text= column[0].strip(),
                        Coach = Coach.objects.get(id=int(column[2].strip())),
                        id = int(column[3].strip()),
                    )
                    match_tags = Match.objects.filter(id__in=match_ids)
                    post.match_tag.set(match_tags)
                
                except ValueError as e:
                    messages.error(request, f"{column} Satırını İşlerken Bir Hata Meydana Geldi: {e}")
                    return render(request, template)
                
            messages.success(request, "Postlar csv dosyası başarıyla yüklendi")
            return render(request, template)

        else:
            messages.error(request, "Böyle bir import yok!")
            return render(request, template)
    

    

    context = {}
    return render(request, template, context)

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
