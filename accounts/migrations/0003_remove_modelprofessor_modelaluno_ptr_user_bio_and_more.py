# Generated by Django 4.1 on 2022-08-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_redefinir_senha_expira_em_redefinir_senha_horario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelprofessor',
            name='modelaluno_ptr',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Uma descrição sobre voce'),
        ),
        migrations.DeleteModel(
            name='modelaluno',
        ),
        migrations.DeleteModel(
            name='modelprofessor',
        ),
    ]
