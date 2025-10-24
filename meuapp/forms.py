from django import forms
from .models import Usuario , Acesso

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['matricula', 'nome_usuario']  
        widgets = {
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Matrícula'
            }),
            'nome_usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
        }
        labels = {
            'matricula': 'Matrícula',
            'nome_usuario': 'Nome do Usuário',
        }

class AcessoForm(forms.ModelForm):
    class Meta:
        model = Acesso
        fields = ['usuario', 'data_acesso', 'desc_evento', 'desc_area', 'desc_leitor', 'ent_sai']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'data_acesso': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'desc_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'desc_area': forms.TextInput(attrs={'class': 'form-control'}),
            'desc_leitor': forms.TextInput(attrs={'class': 'form-control'}),
            'ent_sai': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'usuario': 'Usuário',
            'data_acesso': 'Data de Acesso',
            'desc_evento': 'Descrição do Evento',
            'desc_area': 'Descrição da Área',
            'desc_leitor': 'Descrição do Leitor',
            'ent_sai': 'Entrada/Saída',
        }

class CarregaAcessoForm(forms.Form):
    arquivo = forms.FileField( # Campo para upload de arquivo
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), 
        label='Selecione o arquivo' 
    )

class ListarAcessosForm(forms.Form):
    acesso = forms.ModelChoiceField(
        queryset=Acesso.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Selecione o Acesso'
    )


class UsuarioFiltroForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        required=False,
        label="Selecionar Usuário"
    )
