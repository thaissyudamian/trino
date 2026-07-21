from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Profile, Post, Follow, Comment, Like
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
    curtidos_ids = list(Like.objects.filter(user=request.user).values_list("post", flat=True))
    return render(request, "posts/feed.html", {"posts": posts, "curtidos_ids": curtidos_ids})



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

def explorar(request):
    if not request.user.is_authenticated:
        return redirect("entrar")
    seguindo_ids = list(
        Follow.objects.filter(follower=request.user).values_list("following", flat=True)
    )
    usuarios = User.objects.exclude(id=request.user.id)
    return render(request, "posts/explorar.html", {"usuarios": usuarios, "seguindo_ids": seguindo_ids})


def seguir(request, user_id):
    if request.user.is_authenticated and request.method == "POST":
        alvo = User.objects.get(id=user_id)
        if alvo != request.user:
            Follow.objects.get_or_create(follower=request.user, following=alvo)
    return redirect("explorar")


def deixar_de_seguir(request, user_id):
    if request.user.is_authenticated and request.method == "POST":
        Follow.objects.filter(follower=request.user, following_id=user_id).delete()
    return redirect("explorar")

def perfil(request):
    if not request.user.is_authenticated:
        return redirect("entrar")
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        request.user.first_name = request.POST.get("name", "")
        request.user.save()
        profile.bio = request.POST.get("bio", "")
        if request.FILES.get("photo"):
            profile.photo = request.FILES["photo"]
        profile.save()
        return redirect("perfil")
    posts = Post.objects.filter(author=request.user).order_by("-created_at")
    n_seguindo = Follow.objects.filter(follower=request.user).count()
    n_seguidores = Follow.objects.filter(following=request.user).count()
    return render(request, "posts/perfil.html", {
        "profile": profile,
        "posts": posts,
        "n_seguindo": n_seguindo,
        "n_seguidores": n_seguidores,
    })

def trocar_senha(request):
    if not request.user.is_authenticated:
        return redirect("entrar")
    if request.method == "POST":
        old = request.POST["old_password"]
        new = request.POST["new_password"]
        if not request.user.check_password(old):
            return render(request, "posts/trocar_senha.html", {"erro": "Senha atual incorreta."})
        request.user.set_password(new)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, "posts/trocar_senha.html", {"sucesso": "Senha alterada com sucesso!"})
    return render(request, "posts/trocar_senha.html")

def post_detalhe(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("entrar")
        content = request.POST.get("content", "").strip()
        if content:
            Comment.objects.create(author=request.user, post=post, content=content)
        return redirect("post_detalhe", post_id=post.id)
    comentarios = post.comments.all().order_by("created_at")
    ja_curtiu = request.user.is_authenticated and post.likes.filter(user=request.user).exists()
    return render(request, "posts/post_detalhe.html", {"post": post, "comentarios": comentarios, "ja_curtiu": ja_curtiu})

def curtir(request, post_id):
    if request.user.is_authenticated and request.method == "POST":
        post = Post.objects.get(id=post_id)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            like.delete()
        else:
            Like.objects.create(user=request.user, post=post)
    return redirect(request.POST.get("next") or "home")

def conexoes(request):
    if not request.user.is_authenticated:
        return redirect("entrar")
    seguindo = Follow.objects.filter(follower=request.user).select_related("following")
    seguidores = Follow.objects.filter(following=request.user).select_related("follower")
    return render(request, "posts/conexoes.html", {"seguindo": seguindo, "seguidores": seguidores})

