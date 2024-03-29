# Generated by Django 4.1 on 2022-09-26 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("forum", "0006_alter_respostas_autor_alter_respostas_topico"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="resposta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="like_r",
                to="forum.respostas",
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="like",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
