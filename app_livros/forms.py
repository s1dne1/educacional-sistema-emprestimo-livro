from django import forms
from .models import Livro, Emprestimo


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'ano_publicacao', 'isbn', 'genero',
                  'num_paginas', 'data_aquisicao', 'descricao', 'quantidade', 'disponivel']


# 📌 Formulário para Cadastro de Empréstimos
class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro']
