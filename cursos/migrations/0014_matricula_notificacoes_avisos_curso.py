# Generated by Django 4.1 on 2022-09-09 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0013_modulo_curso_numero_modulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='matricula',
            name='notificacoes',
            field=models.BooleanField(default=True, verbose_name='deseja receber notificações do curso'),
        ),
        migrations.CreateModel(
            name='avisos_curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo do modulo')),
                ('assunto', models.TextField(verbose_name='Assunto')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em: ')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='atualizado em: ')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='avisos', to='cursos.modelcursos')),
            ],
            options={
                'verbose_name': 'Aviso',
                'verbose_name_plural': 'Avisos',
            },
        ),
    ]