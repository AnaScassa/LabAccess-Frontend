import os
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from django.shortcuts import render, redirect
from .forms import CarregaAcessoForm, UsuarioForm, AcessoForm
from .models import Usuario, Acesso
from .forms import UsuarioFiltroForm
from django.http import JsonResponse

def tabela_view(request):
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'meuapp', 'dados', 'relatorio.xls')
    df = pd.read_excel(caminho_arquivo, engine='xlrd')
    html = df.to_html()
    return HttpResponse(html)


class UsuarioCreateView(FormView):
    template_name = 'cadastrar_usuario.html'  
    form_class = UsuarioForm  
    success_url = reverse_lazy('cadastrar_usuario')  

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)
    
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'lista_usuarios.html'  
    context_object_name = 'usuarios'

class AcessoCreateView(FormView):
    template_name = 'cadastrar_acesso.html'  
    form_class = AcessoForm 
    success_url = reverse_lazy('cadastrar_acesso')  

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)

class CarregarAcesso(FormView):
    template_name = 'carregar_acesso.html' # Template para upload
    form_class = CarregaAcessoForm # Formulário de upload
    success_url = reverse_lazy('carregar_acesso') # Redireciona para a mesma página após o upload

    def form_valid(self, form): # Processa o arquivo após o upload
        arquivo = self.request.FILES['arquivo'] # Obtém o arquivo enviado

        # Verifica se é .xls
        if not arquivo.name.endswith('.xls'):
            return render(self.request, self.template_name, { # Renderiza o template com erro
                'form': form, 
                'erro': 'Apenas arquivos .xls são permitidos.' 
            })

        try:
            # Lê planilha XLS usando xlrd
            df = pd.read_excel(arquivo, engine='xlrd')
        except Exception as e:
            return render(self.request, self.template_name, {  
                'form': form,
                'erro': f'Erro ao processar planilha: {e}'
            })

        # Cria usuários e acessos
        for _, row in df.iterrows(): # Itera sobre as linhas da planilha
            categoria = str(row.get('MATRICULA', ''))[:3]
            

            try:
                usuario = Usuario.objects.get(matricula=row.get('MATRICULA', ''))
            except Usuario.DoesNotExist:
                usuario = Usuario.objects.create(
                    matricula=row.get('MATRICULA', ''),
                    nome_usuario=row.get('NOME_ALUNO', 'Desconhecido'),
                    categoriaUsuario=categoria
                )

            Acesso.objects.create( # Cria o registro de acesso
                usuario=usuario,
                data_acesso=row.get('DATA'),
                desc_evento=row.get('DESC_EVENTO', ''),
                desc_area=row.get('DESC_AREA', ''),
                desc_leitor=row.get('DESC_LEITOR', ''),
                ent_sai=row.get('ENT_SAI', '')
            )

        # Gera tabela HTML para exibição
        tabela_html = df.to_html(
            classes='table table-bordered table-striped table-hover',
            index=False
        )

        return render(self.request, 'pagina_planilha.html', {
            'tabela_html': tabela_html
        })



class PaginaPlanilhaView(TemplateView):
    template_name = 'pagina_planilha.html'

    def get(self, request, *args, **kwargs): 
        tabela_html = request.session.get('tabela_html', '<p>Nenhum dado carregado.</p>')
        return render(request, self.template_name, {'tabela_html': tabela_html})
    
class ListaAcessosView(FormView):
    template_name = 'lista_acessos.html' 
    form_class = UsuarioFiltroForm

    def form_valid(self, form): 
        usuario = form.cleaned_data['usuario'] # Obtém o usuário selecionado
        acessos = Acesso.objects.filter(usuario=usuario).values( # Filtra acessos do usuário
            'data_acesso', 'desc_evento', 'desc_area', 'desc_leitor', 'ent_sai'
        )
        return JsonResponse(list(acessos), safe=False) # Retorna dados em JSON
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
class TempoPermanenciaView(TemplateView):
    template_name = 'tempo_permanencia.html'
    form_class = UsuarioFiltroForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'permanencias': []})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        permanencias = []

        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')

            # Filtra acessos
            acessos = Acesso.objects.filter(desc_area='CCS_LAB')
            if usuario:
                acessos = acessos.filter(usuario=usuario)

            # Agrupa acessos por usuário
            acesso_dict = {}
            for acesso in acessos:
                matricula = acesso.usuario.matricula
                if matricula not in acesso_dict:
                    acesso_dict[matricula] = []
                acesso_dict[matricula].append(acesso)

            # Ordena os acessos de cada usuário por data
            for matricula, acessos_usuario in acesso_dict.items():
                acessos_usuario.sort(key=lambda x: x.data_acesso)

            # Calcula tempo de permanência considerando apenas o mesmo dia
            for matricula, acessos_usuario in acesso_dict.items():
                i = 0
                #esse while ele percorre todos os acessos do usuario e depois faz a verificação do ent_sai para calcular o tempo de permanência
                while i < len(acessos_usuario): 
                    # se for entrada e saida no mesmo dia, ignora a próxima entrada  
                    if acessos_usuario[i].ent_sai == '1':  # é entrada
                        # procura a próxima saída válida
                        j = i + 1
                        while j < len(acessos_usuario) and acessos_usuario[j].ent_sai != '0':
                            j += 1

                        if j < len(acessos_usuario):
                            entrada = acessos_usuario[i]
                            saida = acessos_usuario[j]

                            # Verifica se a entrada e saída são do mesmo dia
                            if entrada.data_acesso.date() == saida.data_acesso.date():
                                tempo_permanencia = saida.data_acesso - entrada.data_acesso
                                permanencias.append({
                                    'usuario': entrada.usuario.nome_usuario,
                                    'matricula': entrada.usuario.matricula,
                                    'entrada': entrada.data_acesso,
                                    'saida': saida.data_acesso,
                                    'tempo_permanencia': tempo_permanencia
                                })
                            i = j + 1
                        else:
                            break  
                    else:
                        i += 1  

        return render(request, self.template_name, {'form': form, 'permanencias': permanencias})

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------