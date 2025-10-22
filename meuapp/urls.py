from django.urls import path
from . import views

urlpatterns = [
    path('tabela/', views.tabela_view, name='tabela'),
    path('cadastrar_usuario/', views.UsuarioCreateView.as_view(), name='cadastrar_usuario'),
]
