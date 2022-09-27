from dataclasses import fields
import site
from django.contrib import admin

# Register your models here.
from .models import *

class cusosadmin(admin.ModelAdmin): #faz a customização dos models

    list_display =  ['nome','slug','data_inicio','criado_em'] #personaliza no campos que sao mostrados
    search_fields= ['nome','slug'] #cria um modulo de busca, que busca items da tabela com forme os campos passados
    prepopulated_fields= {'slug': ('nome',)}

admin.site.register(modelcursos,cusosadmin) #adciona tabela cursos no admin

admin.site.register([matricula,categoria_curso
,modulo_curso,aulas_curso,avisos_curso,materiais_curso]) #adciona tabela cursos no admin
