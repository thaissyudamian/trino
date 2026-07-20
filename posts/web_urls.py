from django.urls import path

from . import web

urlpatterns = [
    path("", web.home, name="home"),
    path("cadastro/", web.cadastro, name="cadastro"),
    path("entrar/", web.entrar, name="entrar"),
    path("sair/", web.sair, name="sair"),
    path("explorar/", web.explorar, name="explorar"),
    path("seguir/<int:user_id>/", web.seguir, name="seguir"),
    path("deixar-de-seguir/<int:user_id>/", web.deixar_de_seguir, name="deixar_de_seguir"),
    path("perfil/", web.perfil, name="perfil"),
    path("trocar-senha/", web.trocar_senha, name="trocar_senha"),
    path("post/<int:post_id>/", web.post_detalhe, name="post_detalhe"),
    path("curtir/<int:post_id>/", web.curtir, name="curtir"),




]
