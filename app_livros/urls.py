from django.urls import path
from . import views
from .views import listar_leitores, cadastrar_leitor,editar_leitor,excluir_leitor


urlpatterns = [
    path('', views.home, name='home'),
    path('livros/', views.lista_livros, name='lista_livros'),
    path('livros/cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('emprestar/<int:livro_id>/', views.emprestar_livro, name='emprestar_livro'),
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('devolver/<int:emprestimo_id>/', views.devolver_livro, name='devolver_livro'),
    path('leitores/', listar_leitores, name='listar_leitores'),
    path('leitores/novo/', cadastrar_leitor, name='cadastrar_leitor'),
    path('leitores/<int:pk>/editar/', editar_leitor, name='editar_leitor'),
    path('leitores/<int:pk>/excluir/', excluir_leitor, name='excluir_leitor'),
    path('livros/editar/<int:livro_id>/', views.editar_livro, name='editar_livro'),
    path('livros/excluir/<int:livro_id>/', views.excluir_livro, name='excluir_livro'),
]
