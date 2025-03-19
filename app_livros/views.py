from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm

# 📌 Página Inicial
def home(request):
    return render(request, 'home.html')

# 📌 Listar Livros Disponíveis
@login_required
def lista_livros(request):
    livros = Livro.objects.filter(disponivel=True)
    return render(request, 'livro_list.html', {'livros': livros})

# 📌 Cadastrar um Novo Livro (Apenas Bibliotecários)
@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = LivroForm()
    return render(request, 'cadastrar_livro.html', {'form': form})

# 📌 Emprestar um Livro
@login_required
def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id, disponivel=True)
    if request.method == 'POST':
        livro.disponivel = False
        livro.save()
        Emprestimo.objects.create(usuario=request.user, livro=livro)
        return redirect('lista_livros')
    return render(request, 'emprestar_confirm.html', {'livro': livro})

# 📌 Listar Empréstimos do Usuário
@login_required
def lista_emprestimos(request):
    emprestimos = Emprestimo.objects.filter(usuario=request.user)
    return render(request, 'emprestimo_list.html', {'emprestimos': emprestimos})

# 📌 Devolver um Livro
@login_required
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, usuario=request.user)
    if request.method == 'POST':
        emprestimo.livro.disponivel = True
        emprestimo.livro.save()
        emprestimo.data_devolucao = timezone.now().date()
        emprestimo.devolvido = True
        emprestimo.save()
        return redirect('lista_emprestimos')
    return render(request, 'devolver_confirm.html', {'emprestimo': emprestimo})
