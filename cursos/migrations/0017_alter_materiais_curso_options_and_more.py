# Generated by Django 4.1 on 2022-09-10 14:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0016_alter_avisos_curso_titulo_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materiais_curso',
            options={'verbose_name': 'Materiais do curso'},
        ),
        migrations.AlterField(
            model_name='materiais_curso',
            name='material',
            field=models.FileField(upload_to='cursos/materiais', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'pptx'])], verbose_name='Material'),
        ),
    ]
