# Generated by Django 4.0.6 on 2022-08-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='imageperfil',
            field=models.ImageField(blank=True, null=True, upload_to='perfil/imagens', verbose_name='imagem perfil'),
        ),
        migrations.AddField(
            model_name='user',
            name='nome',
            field=models.CharField(max_length=100, null=True, verbose_name='Nome completo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='E-mail'),
        ),
    ]
