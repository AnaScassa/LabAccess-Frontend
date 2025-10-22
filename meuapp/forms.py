from django import forms
from .models import Usuario  

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['matricula', 'nome_usuario']  
        widgets = {
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a matrícula'
            }),
            'nome_usuario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do usuário'
            }),
        }
        labels = {
            'matricula': 'Matrícula',
            'nome_usuario': 'Nome do Usuário',
        }
