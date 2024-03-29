# Generated by Django 4.1 on 2022-08-26 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cursos', '0003_matricula'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matricula',
            options={'verbose_name': 'Matricula', 'verbose_name_plural': 'Matriculas'},
        ),
        migrations.AlterField(
            model_name='matricula',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matricula', to='cursos.modelcursos'),
        ),
        migrations.AlterField(
            model_name='matricula',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matricula', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='matricula',
            unique_together={('user', 'curso')},
        ),
    ]
