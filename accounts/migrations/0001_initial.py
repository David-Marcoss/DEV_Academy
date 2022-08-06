# Generated by Django 4.0.6 on 2022-08-06 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='modelaluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, null=True, verbose_name='Nome completo')),
                ('imageperfil', models.ImageField(blank=True, null=True, upload_to='perfil/imagens', verbose_name='imagem')),
                ('perfil', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='modelprofessor',
            fields=[
                ('modelaluno_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.modelaluno')),
                ('qualificacao', models.CharField(max_length=200, null=True, verbose_name='Qualificação')),
            ],
            bases=('accounts.modelaluno',),
        ),
    ]
