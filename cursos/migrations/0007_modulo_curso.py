# Generated by Django 4.1 on 2022-09-01 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0006_modelcursos_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='modulo_curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo do modulo')),
                ('status_modulo', models.BooleanField(default=False, verbose_name='Status do modulo:')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em: ')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='atualizado em: ')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='modulo', to='cursos.modelcursos')),
            ],
            options={
                'verbose_name': 'Modulo',
                'verbose_name_plural': 'Modulos',
            },
        ),
    ]
