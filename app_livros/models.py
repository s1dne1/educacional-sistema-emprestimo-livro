from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from django.db import models

from django.db import models
from django.core.exceptions import ValidationError

class Livro(models.Model):
    GENEROS_CHOICES = [
        # Ficção
        ('Romance', 'Romance'),
        ('Aventura', 'Aventura'),
        ('Fantasia', 'Fantasia'),
        ('Ficção Científica', 'Ficção Científica'),
        ('Distopia', 'Distopia'),
        ('Suspense', 'Suspense'),
        ('Mistério', 'Mistério'),
        ('Terror', 'Terror'),
        ('Policial', 'Policial'),
        ('Drama', 'Drama'),
        ('Humor', 'Humor'),
        ('Realismo Mágico', 'Realismo Mágico'),

        # Não Ficção
        ('História', 'História'),
        ('Filosofia', 'Filosofia'),
        ('Psicologia', 'Psicologia'),
        ('Sociologia', 'Sociologia'),
        ('Política', 'Política'),
        ('Economia', 'Economia'),
        ('Religião', 'Religião'),
        ('Espiritualidade', 'Espiritualidade'),
        ('Educação', 'Educação'),
        ('Autoajuda', 'Autoajuda'),
        ('Negócios', 'Negócios'),
        ('Marketing', 'Marketing'),
        ('Tecnologia', 'Tecnologia'),
        ('Ciência', 'Ciência'),
        ('Saúde', 'Saúde'),
        ('Meio Ambiente', 'Meio Ambiente'),
        ('Direito', 'Direito'),

        # Infantil / Juvenil
        ('Infantil', 'Infantil'),
        ('Infantojuvenil', 'Infantojuvenil'),
        ('Conto de Fadas', 'Conto de Fadas'),
        ('Fábulas', 'Fábulas'),

        # Outros
        ('Poesia', 'Poesia'),
        ('Teatro', 'Teatro'),
        ('HQ/Mangá', 'HQ / Mangá'),
        ('Clássico', 'Clássico'),
        ('Ensaio', 'Ensaio'),
        ('Antologia', 'Antologia'),
        ('Manual', 'Manual'),
        ('Técnico', 'Técnico'),
        ('Didático', 'Didático'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editora = models.CharField(max_length=100, blank=True, null=True)
    ano_publicacao = models.IntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    genero = models.CharField(max_length=100, choices=GENEROS_CHOICES, blank=True, null=True)
    num_paginas = models.IntegerField(blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=1)
    disponivel = models.BooleanField(default=True)
    tombamento = models.PositiveBigIntegerField(default=1)
    observacao = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano_publicacao})"
    
    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        if Livro.objects.exclude(pk=self.pk).filter(isbn=self.isbn).exists():
            raise ValidationError({'isbn': 'Já existe um livro cadastrado com este ISBN.'})




# 📌 Cadastro de Empréstimos
class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Quem pegou o livro
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    leitor = models.ForeignKey('Leitor', on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_prevista_devolucao = models.DateField(default=timezone.now() + timedelta(days=7))
    data_devolucao = models.DateField(null=True, blank=True)
    estado_conservacao = models.CharField(
    max_length=50,
    choices=[
        ('ótimo', 'Ótimo'),
        ('bom', 'Bom'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim'),
        ('danificado', 'Danificado')
    ],
    blank=True,
    null=True
)

    observacoes_conservacao = models.TextField(blank=True, null=True)
   

    def __str__(self):
        return f"{self.leitor} - {self.livro.titulo}"

    @property
    def statusprazo(self):
        if self.data_devolucao:
            return 'devolvido'
        elif self.data_prevista_devolucao < date.today():
            return 'vencido'
        elif (self.data_prevista_devolucao - date.today()).days <= 3:
            return 'avencer'
        else:
            return 'noprazo'
        
class Leitor(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    turma = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)  

    def __str__(self):
        return f"{self.nome} ({self.turma})"
    