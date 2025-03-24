from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Livro, Emprestimo, Leitor
from .forms import LivroForm, EmprestimoForm, LeitorForm
from django.utils import timezone
from django.db.models import Q


# 📌 Página Inicial
def home(request):
    return render(request, 'home.html')

# 📌 Listar Livros Disponíveis
@login_required
def lista_livros(request):
    busca = request.GET.get('busca')
    disponibilidade = request.GET.get('disponivel')

    livros = Livro.objects.all()

    # Filtro por título, autor ou gênero
    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) |
            Q(autor__icontains=busca) |
            Q(genero__icontains=busca)
        )

    livros_filtrados = []
    for livro in livros:
        emprestimo_ativo = Emprestimo.objects.filter(livro=livro, data_devolucao__isnull=True).first()

        livro.emprestado = bool(emprestimo_ativo)
        livro.emprestimo = emprestimo_ativo

        # Filtro adicional de disponibilidade
        if disponibilidade == 'disponiveis' and (livro.emprestado or not livro.disponivel):
            continue
        elif disponibilidade == 'emprestados' and (not livro.emprestado or not livro.disponivel):
            continue
        elif disponibilidade == 'baixados' and livro.disponivel:
            continue

        livros_filtrados.append(livro)

    paginator = Paginator(livros_filtrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'livro_list.html', {
        'page_obj': page_obj,
        'busca': busca,
        'disponibilidade': disponibilidade
    })



 
# 📌 Cadastrar um Novo Livro (Apenas Bibliotecários)
@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Livro cadastrado com sucesso!")
            return redirect('lista_livros')
        else:
            print(form.errors)        
    else:
        form = LivroForm()
    return render(request, 'cadastrar_livro.html', {'form': form})

# 📌 Emprestar um Livro
@login_required
def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id, disponivel=True)
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.livro = livro
            emprestimo.usuario = request.user
            emprestimo.save()
            livro.save()

            messages.success(request, "Livro emprestado com sucesso!")
            return redirect('lista_livros')
    else:
        form = EmprestimoForm()
    return render(request,'emprestar_confirm.html',{'livro':livro,'form':form})
        
from django.core.paginator import Paginator

@login_required
def lista_emprestimos(request):
    busca = request.GET.get('busca')
    statusprazo = request.GET.get('statusprazo')

    emprestimos = Emprestimo.objects.all()

    if busca:
        emprestimos = emprestimos.filter(
            Q(livro__titulo__icontains=busca) |
            Q(livro__autor__icontains=busca) |
            Q(leitor__nome__icontains=busca)
        )

    if statusprazo:
        emprestimos = [e for e in emprestimos if e.statusprazo == statusprazo]

    # 📌 Paginação aqui
    paginator = Paginator(emprestimos, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'emprestimo_list.html', {
        'page_obj': page_obj,
        'busca': busca,
        'statusprazo': statusprazo
    })



# 📌 Devolver um Livro
@login_required
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id, data_devolucao__isnull=True)

    if request.method == 'POST':
        estado = request.POST.get('estado_conservacao')
        comentario = request.POST.get('comentario')

        emprestimo.data_devolucao = timezone.now()
        emprestimo.estado_conservacao = estado
        emprestimo.observacoes_conservacao = comentario
        emprestimo.save()

        livro = emprestimo.livro
        livro.disponivel = True
        livro.save()

        messages.success(request, 'Livro devolvido com sucesso!')
        return redirect('lista_livros')

    return render(request, 'devolver_confirm.html', {
        'emprestimo': emprestimo
    })

from django.core.paginator import Paginator
from .models import Leitor
from .forms import LeitorForm

@login_required
def listar_leitores(request):
    busca = request.GET.get('busca')
    leitores = Leitor.objects.all()

    if busca:
        leitores = leitores.filter(
            Q(nome__icontains=busca) | Q(cpf__icontains=busca)
        )

    paginator = Paginator(leitores, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listar_leitores.html', {
        'page_obj': page_obj,
        'busca': busca
    })


@login_required
def cadastrar_leitor(request):

    if request.method == 'POST':
        form = LeitorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leitor cadastrado com sucesso!")
            return redirect('listar_leitores')
    else:
        form = LeitorForm()

    return render(request, 'cadastrar_leitor.html', {'form': form})


@login_required
def editar_leitor(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    if request.method == 'POST':
        form = LeitorForm(request.POST, instance=leitor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leitor atualizado com sucesso!')
            return redirect('listar_leitores')
    else:
        form = LeitorForm(instance=leitor)
    return render(request, 'cadastrar_leitor.html', {'form': form, 'editar': True})

@login_required
def excluir_leitor(request, pk):
    leitor = get_object_or_404(Leitor, pk=pk)
    leitor.delete()
    messages.success(request, 'Leitor excluído com sucesso!')
    return redirect('listar_leitores')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Livro
from .forms import LivroForm
from django.contrib import messages

# 📌 Editar Livro
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)  # ESSENCIAL
        form.instance.pk = livro.pk  # FORÇA vinculação correta
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro atualizado com sucesso!')
            return redirect('lista_livros')
        else:
            print("Form inválido:", form.errors)
            print("PK do livro sendo editado:", livro.pk)
            print("ISBN digitado:", request.POST.get('isbn'))   
            print("Livro no banco com esse ISBN:", Livro.objects.filter(isbn=request.POST.get('isbn')).values())
    else:
        form = LivroForm(instance=livro)

    return render(request, 'cadastrar_livro.html', {'form': form, 'editar': True})


# 📌 Excluir Livro
@login_required
@login_required
def excluir_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    # Verifica se o livro já foi emprestado alguma vez
    teve_emprestimo = Emprestimo.objects.filter(livro=livro).exists()

    if teve_emprestimo:
        messages.error(request, f'O livro "{livro.titulo}" não pode ser excluído porque já foi emprestado.')
    else:
        livro.delete()
        messages.success(request, f'Livro "{livro.titulo}" excluído com sucesso!')

    return redirect('lista_livros')
