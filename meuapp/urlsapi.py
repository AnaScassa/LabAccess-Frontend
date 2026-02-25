from django.urls import include, path
from rest_framework import routers
from meuapp.api import AcessoViewSet, GroupViewSet, UserViewSet, UsuarioViewSet
from .apiview import carregar_acesso, lista_acessos
from api.apiview import UserViewSetApi

router = routers.DefaultRouter()
router.register(r"users", UserViewSet) 
router.register(r"groups", GroupViewSet)
router.register(r"acessos", AcessoViewSet)
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("upload-xls/", carregar_acesso),
]
