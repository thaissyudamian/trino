from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Profile, Post, Follow
from django.db.models import Q



def home(request):
    if not request.user.is_authenticated:
        return render(request, "posts/home.html")
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Post.objects.create(author=request.user, content=content)
        return redirect("home")
    seguindo = Follow.objects.filter(follower=request.user).values_list("following", flat=True)
    posts = Post.objects.filter(
        Q(author__in=seguindo) | Q(author=request.user)
    ).order_by("-created_at")
    return render(request, "posts/feed.html", {"posts": posts})



def cadastro(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            return render(request, "posts/cadastro.html", {"erro": "Esse nome de usuário já existe."})
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)
        login(request, user)
        return redirect("home")
    return render(request, "posts/cadastro.html")


def entrar(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        return render(request, "posts/entrar.html", {"erro": "Usuário ou senha inválidos."})
    return render(request, "posts/entrar.html")


def sair(request):
    logout(request)
    return redirect("home")
