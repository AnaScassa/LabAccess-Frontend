import os
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from .forms import CarregaAcessoForm, UsuarioForm, AcessoForm, AcessoCrispy
from .models import Usuario, Acesso
from .forms import UsuarioFiltroForm
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from .forms import ContatoForm
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
    template_name = 'carregar_acesso.html'
    form_class = CarregaAcessoForm
    success_url = reverse_lazy('carregar_acesso')

    def form_valid(self, form):
        arquivo = self.request.FILES['arquivo']

        # Verifica se é .xls
        if not arquivo.name.endswith('.xls'):
            return render(self.request, self.template_name, {
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

        novos_registros = 0
        duplicados = 0

        for _, row in df.iterrows():
            categoria = str(row.get('MATRICULA', ''))[:3]

            # Verifica se o usuário já existe ou cria
            usuario, _ = Usuario.objects.get_or_create(
                matricula=row.get('MATRICULA', ''),
                defaults={
                    'nome_usuario': row.get('NOME_ALUNO', 'Desconhecido'),
                    'categoriaUsuario': categoria
                }
            )

            # Converte a data com fuso horário
            data = timezone.make_aware(row.get('DATA'))

            # Cria ou ignora duplicados (graças ao unique_together no model)
            _,created = Acesso.objects.get_or_create(
                usuario=usuario,
                data_acesso=data,
                desc_evento=row.get('DESC_EVENTO', ''),
                desc_area=row.get('DESC_AREA', ''),
                desc_leitor=row.get('DESC_LEITOR', ''),
                ent_sai=row.get('ENT_SAI', '')
            )

            if created:
                novos_registros += 1
            else:
                duplicados += 1

        tabela_html = df.to_html(
            classes='table table-bordered table-striped table-hover',
            index=False
        )

        mensagem = f"{novos_registros} novos registros inseridos."
        if duplicados > 0:
            mensagem += f" {duplicados} registros já existiam e foram ignorados."

        return render(self.request, 'pagina_planilha.html', {
            'tabela_html': tabela_html,
            'mensagem': mensagem
        })

def CarregaAcessoCrispy(request):
    form = AcessoCrispy(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        arquivo = request.FILES['arquivo']
        print("Arquivo recebido:", arquivo.name)
        mensagem_sucesso = f"O arquivo {arquivo.name} foi enviado com sucesso!"
        return render(request, 'carrega_acesso_crispy.html', {'form': form, 'mensagem_sucesso': mensagem_sucesso})
    return render(request, 'carrega_acesso_crispy.html', {'form': form})

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
            porta = form.cleaned_data.get('porta')
            data = request.POST.get('data')  


            if porta == 'ccs':
                acessos = Acesso.objects.filter(desc_area='CCS')
            elif porta == 'ccs_lab':
                acessos = Acesso.objects.filter(desc_area='CCS_LAB')
            elif porta == 'todos':
                acessos = Acesso.objects.all()
            else:
                acessos = Acesso.objects.none()

            if usuario:
                acessos = acessos.filter(usuario=usuario)

            if data:
                try:
                    data_formatada = timezone.make_aware(datetime.strptime(data, "%Y-%m-%d").date())
                    acessos = acessos.filter(data_acesso__date=data_formatada)
                except ValueError:
                    pass  

            acesso_dict = {}
            for acesso in acessos:
                matricula = acesso.usuario.matricula
                if matricula not in acesso_dict:
                    acesso_dict[matricula] = []
                acesso_dict[matricula].append(acesso)

            for matricula, acessos_usuario in acesso_dict.items():
                acessos_usuario.sort(key=lambda x: x.data_acesso)
                filtrados = []
                anterior = None
                for acesso in acessos_usuario:
                    if anterior and acesso.ent_sai == anterior.ent_sai and acesso.desc_area == anterior.desc_area:
                        diferenca_segundos = (acesso.data_acesso - anterior.data_acesso).total_seconds()
                        if diferenca_segundos < 300:
                            anterior = acesso
                            continue
                    filtrados.append(acesso)
                    anterior = acesso
                acesso_dict[matricula] = filtrados

            permanencias = self.processaAcessos(acesso_dict)
            
        return render(request, self.template_name, {'form': form, 'permanencias': permanencias})

    def processaAcessos(self, acesso_dict):
        permanencias = []
        for matricula, acessos_usuario in acesso_dict.items():
            i = 0
            while i < len(acessos_usuario):
                acesso_atual = acessos_usuario[i]
                if acesso_atual.ent_sai == '1':  # ENTRADA
                    j = i + 1
                    while j < len(acessos_usuario) and acessos_usuario[j].ent_sai != '0':
                        j += 1
                    if j < len(acessos_usuario):
                        entrada = acesso_atual
                        saida = acessos_usuario[j]
                        if entrada.data_acesso.date() == saida.data_acesso.date():
                            tempo = saida.data_acesso - entrada.data_acesso
                            permanencias.append({
                                'usuario': entrada.usuario.nome_usuario,
                                'matricula': entrada.usuario.matricula,
                                'entrada': entrada.data_acesso,
                                'saida': saida.data_acesso,
                                'tempo_permanencia': tempo,
                                'ocorrencia': entrada.desc_evento,
                                'porta': entrada.desc_area
                            })
                            i = j + 1
                        else:
                            permanencias.append({
                                'usuario': entrada.usuario.nome_usuario,
                                'matricula': entrada.usuario.matricula,
                                'entrada': entrada.data_acesso,
                                'saida': None,
                                'tempo_permanencia': 'Indisponível',
                                'ocorrencia': entrada.desc_evento + " - Saída em outro dia",
                                'porta': entrada.desc_area
                            })
                            i += 1
                    else:
                        permanencias.append({
                            'usuario': acesso_atual.usuario.nome_usuario,
                            'matricula': acesso_atual.usuario.matricula,
                            'entrada': acesso_atual.data_acesso,
                            'saida': None,
                            'tempo_permanencia': 'Indisponível',
                            'ocorrencia': acesso_atual.desc_evento + " - Entrada sem saída",
                            'porta': acesso_atual.desc_area
                        })
                        break
                elif acesso_atual.ent_sai == '0':
                    permanencias.append({
                        'usuario': acesso_atual.usuario.nome_usuario,
                        'matricula': acesso_atual.usuario.matricula,
                        'entrada': None,
                        'saida': acesso_atual.data_acesso,
                        'tempo_permanencia': 'Indisponível',
                        'ocorrencia': acesso_atual.desc_evento + " - Saída sem entrada",
                        'porta': acesso_atual.desc_area
                    })
                    i += 1
                else:
                    i += 1
        return permanencias
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def exemplo_crispy(request):
    form = ContatoForm() 
    return render(request, 'crispy.html', {'form': form})

def contato_view(request):
    form = ContatoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        nome = form.cleaned_data['nome']
        email = form.cleaned_data['email']
        mensagem = form.cleaned_data['mensagem']

        print(f"Mensagem de {nome} ({email}): {mensagem}")

        return render(request, 'contato.html', {
            'form': ContatoForm(), 
            'mensagem_sucesso': 'Mensagem enviada com sucesso!'
        })

    return render(request, 'contato.html', {'form': form})
