from django.urls import path
from . import views
from .views import CarregarAcesso, PaginaPlanilhaView,  ListaAcessosView, TempoPermanenciaView

urlpatterns = [
    path('tabela/', views.tabela_view, name='tabela'),
    path('cadastrar_usuario/', views.UsuarioCreateView.as_view(), name='cadastrar_usuario'),
    path('lista_usuarios/', views.UsuarioListView.as_view(), name='lista_usuarios'),
    path('cadastrar_acesso/', views.AcessoCreateView.as_view(), name='cadastrar_acesso'),
    path('carregar_acesso/', CarregarAcesso.as_view(), name='carregar_acesso'),    
    path('planilha/', PaginaPlanilhaView.as_view(), name='pagina_planilha'),
    path('lista_acessos/', ListaAcessosView.as_view(), name='lista_acessos'),
    path('tempo_permanencia/', TempoPermanenciaView.as_view(), name='tempo_permanencia'),
    ]
