# Generated by Django 4.1 on 2022-09-08 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0011_aulas_curso_sobre_aula_alter_aulas_curso_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='aulas_curso',
            name='numero_aula',
            field=models.IntegerField(blank=True, default=0, verbose_name='numero aula'),
        ),
    ]