from django import forms
from .models import Livro, Emprestimo, Leitor



class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'num_paginas': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_aquisicao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tombamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacao': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': '500',
                'placeholder': 'Preencha aqui detalhes do livro. Ex: Doação recebida em 2025, do Fulano, item com anotações...'
            }),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        qs = Livro.objects.filter(isbn=isbn)

        # Se estiver editando, exclui ele mesmo da verificação
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Já existe um livro cadastrado com este ISBN.")
        return isbn



# 📌 Formulário para Cadastro de Empréstimos
class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['leitor','data_prevista_devolucao']
        widgets = {
           'data_prevista_devolucao':forms.DateInput(attrs={'type':'date'}),
           'leitor': forms.Select(attrs={'class': 'form-select'}),
           }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leitor'].empty_label = "Selecione um leitor"


class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = '__all__'
        widgets = {
            'telefone': forms.TextInput(attrs={'placeholder': '(11) 91234-5678'}),
        }
