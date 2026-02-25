from django import forms
from django.urls import reverse
from .models import Usuario , Acesso
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Row, Column, Field
from crispy_forms.bootstrap import FormActions

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
    porta = forms.ChoiceField(
        choices=[
            ('ccs', 'ccs'),
            ('ccs_lab', 'ccs_lab'),
            ('todos', 'todos'),
        ],
        widget= forms.RadioSelect(),
        label="Selecionar porta"
    )
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Selecionar Data"
    )

class ExampleForm(forms.Form):
    nome = forms.CharField(label="Seu nome", max_length=100)
    email = forms.EmailField(label="Email")
    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput(), max_length=128)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse("contato") 
        self.helper.add_input(Submit('submit', 'Enviar'))

class AcessoCrispy(forms.Form):
    arquivo = forms.FileField(
        label='Selecione o arquivo',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'carregar_acesso'  
        self.helper.enctype = 'multipart/form-data' 
        #self.helper.add_input(Submit('submit', 'Enviar Arquivo', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Row(
                Field(
                    "arquivo", 
                    wrapper_class= "col-md",
                    template="field.html"

                ), 
                Column(
                    Submit('submit', 'Enviar Arquivo', css_class='btn btn-primary'),
                    css_class= "col-md align-self-end"
                )
            )
        )
