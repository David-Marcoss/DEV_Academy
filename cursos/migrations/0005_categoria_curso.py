# Generated by Django 4.1 on 2022-09-01 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0004_alter_matricula_options_alter_matricula_curso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='categoria_curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=100, verbose_name='Categoria do curso')),
            ],
            options={
                'verbose_name': 'Categoria curso',
                'verbose_name_plural': 'Categorias cursos',
            },
        ),
    ]
