# Generated by Django 5.1.6 on 2025-03-23 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_livros', '0006_livro_tombamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='tombamento',
        ),
    ]
