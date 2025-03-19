from django.db import models
from django.contrib.auth.models import User

from django.db import models

from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editora = models.CharField(max_length=100, blank=True, null=True)
    ano_publicacao = models.IntegerField()
    isbn = models.CharField(max_length=20, unique=True,default=1)
    genero = models.CharField(max_length=100, choices=[
        ('Ficção', 'Ficção'),
        ('Não Ficção', 'Não Ficção'),
        ('Romance', 'Romance'),
        ('Suspense', 'Suspense'),
        ('Aventura', 'Aventura'),
        ('Ciência', 'Ciência'),
        ('História', 'História'),
    ], blank=True, null=True)
    num_paginas = models.IntegerField(blank=True, null=True)
    data_aquisicao = models.DateField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=1)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.ano_publicacao})"



# 📌 Cadastro de Empréstimos
class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Quem pegou o livro
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    devolvido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} pegou {self.livro.titulo}"
