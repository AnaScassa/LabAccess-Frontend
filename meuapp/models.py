from django.db import models

# Create your models here.
#['DATA', 'MATRICULA', 'NOME_ALUNO', 'CD_CARTAO', 'DESC_EVENTO', 'DESC_AREA', 'DESC_LEITOR', 'ENT_SAI']

#model, view para subir o arquivo, view para mostrar os dados, modelo nome usuairo/matricula
#model com outros dados usando usuario, usuario/acesso
#views usar classes form e listview para subir e mostrar os dados 

class Usuario(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    nome_usuario = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome_usuario} ({self.matricula})"


class Acesso(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        to_field='matricula',
        on_delete=models.CASCADE
    )
    data_acesso = models.DateTimeField()
    desc_evento = models.CharField(max_length=100)
    desc_area = models.CharField(max_length=100)
    desc_leitor = models.CharField(max_length=100)
    ent_sai = models.CharField(max_length=10)

    def __str__(self):
        return f"Acesso de {self.usuario.nome_usuario} em {self.data_acesso}"