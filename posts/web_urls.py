from django.urls import path

from . import web

urlpatterns = [
    path("", web.home, name="home"),
    path("cadastro/", web.cadastro, name="cadastro"),
    path("entrar/", web.entrar, name="entrar"),
    path("sair/", web.sair, name="sair"),
]
