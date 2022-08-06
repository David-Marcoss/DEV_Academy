from django.contrib import admin

from .models import modelprofessor,modelaluno

# Register your models here.


admin.site.register(modelprofessor) #adciona tabela cursos no admin
admin.site.register(modelaluno) #adciona tabela cursos no admin

