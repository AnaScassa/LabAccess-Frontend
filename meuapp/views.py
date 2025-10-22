import os
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import UsuarioForm

def tabela_view(request):
    caminho_arquivo = os.path.join(settings.BASE_DIR, 'meuapp', 'dados', 'relatorio.xls')
    df = pd.read_excel(caminho_arquivo, engine='xlrd')
    html = df.to_html()
    return HttpResponse(html)


class UsuarioCreateView(FormView):
    template_name = 'cadastrar_usuario.html'  
    form_class = UsuarioForm  
    success_url = reverse_lazy('listar_usuarios')  

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)
    