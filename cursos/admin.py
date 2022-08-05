from dataclasses import fields
import site
from django.contrib import admin

# Register your models here.
from .models import cursos

class cusosadmin(admin.ModelAdmin): #faz a customização dos models

    list_display =  ['nome','slug','data_inicio','criado_em'] #personaliza no campos que sao mostrados
    search_fields= ['nome','slug'] #cria um modulo de busca, que busca items da tabela com forme os campos passados
    prepopulated_fields= {'slug': ('nome',)}

admin.site.register(cursos,cusosadmin) #adciona tabela cursos no admin