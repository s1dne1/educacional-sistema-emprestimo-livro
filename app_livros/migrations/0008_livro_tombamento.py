# Generated by Django 5.1.6 on 2025-03-23 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_livros', '0007_remove_livro_tombamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='tombamento',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
