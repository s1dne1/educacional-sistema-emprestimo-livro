from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('livros/', views.lista_livros, name='lista_livros'),
    path('livros/cadastrar/', views.cadastrar_livro, name='cadastrar_livro'),
    path('emprestar/<int:livro_id>/', views.emprestar_livro, name='emprestar_livro'),
    path('emprestimos/', views.lista_emprestimos, name='lista_emprestimos'),
    path('devolver/<int:emprestimo_id>/', views.devolver_livro, name='devolver_livro'),
]
