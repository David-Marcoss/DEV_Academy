# Generated by Django 4.1 on 2022-09-27 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0019_categoria_curso_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelcursos',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cursos_c', to='cursos.categoria_curso'),
        ),
    ]
