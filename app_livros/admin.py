from django.contrib import admin
from .models import Livro,Emprestimo
from .models import Leitor



# Register your models here.
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Leitor)