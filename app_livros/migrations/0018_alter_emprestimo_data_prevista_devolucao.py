# Generated by Django 5.1.6 on 2025-05-06 01:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_livros', '0017_alter_emprestimo_data_prevista_devolucao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='data_prevista_devolucao',
            field=models.DateField(default=datetime.datetime(2025, 5, 13, 1, 58, 56, 95880, tzinfo=datetime.timezone.utc)),
        ),
    ]
