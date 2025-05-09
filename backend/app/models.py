
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Fonte(models.Model):
    nome = models.CharField(max_length=200)
    url = models.URLField()
    tipo = models.CharField(max_length=50, choices=[('rss', 'RSS'), ('web', 'Web')])
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Tema(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    palavras_chave = models.TextField(help_text="Separe palavras por vírgulas.")
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Document(models.Model):
    fonte = models.ForeignKey(Fonte, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=300)
    url = models.URLField(blank=True, null=True)
    data_publicacao = models.DateTimeField(blank=True, null=True)
    texto_extraido = models.TextField(blank=True)
    temas = models.ManyToManyField(Tema, blank=True)

    def __str__(self):
        return self.titulo

class DocumentChunk(models.Model):
    documento = models.ForeignKey(Document, on_delete=models.CASCADE)
    texto = models.TextField()
    vetor_id = models.CharField(max_length=100, blank=True, null=True)

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    documento = models.ForeignKey(Document, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "documento")

class Anotacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    documento = models.ForeignKey(Document, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

class FonteLog(models.Model):
    fonte = models.ForeignKey(Fonte, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('sucesso', 'Sucesso'), ('erro', 'Erro')])
    total_documentos = models.PositiveIntegerField(default=0)
    mensagem = models.TextField(blank=True, null=True)

class ConsultaLog(models.Model):
    pergunta = models.TextField()
    resposta = models.TextField()
    contexto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)


from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    TIPO_CHOICES = [
        ("admin", "Administrador"),
        ("analista", "Analista"),
        ("editor", "Editor"),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="analista")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.tipo})"

@receiver(post_save, sender=User)
def criar_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(usuario=instance)
