# Generated by Django 4.0.6 on 2022-08-06 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_modelaluno_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelprofessor',
            name='qualificacao',
            field=models.TextField(max_length=200, null=True, verbose_name='Qualificação'),
        ),
    ]