from cgitb import text
from curses.ascii import NUL
from distutils.command.upload import upload
from distutils.text_file import TextFile
from email.mime import image
from pickle import TRUE
from tabnanny import verbose
from typing import OrderedDict
from typing_extensions import Self
from unicodedata import name
from django.db import models
from django.forms import CharField

from accounts.models import User


class modelcursos(models.Model):

    nome = models.CharField('Titulo do curso',max_length=100)
    descricao = models.TextField('descrição breve',blank=True) #blank indica que o campo nao é obrigatorio
    
    sobre_curso = models.TextField('sobre o curso',blank=True) #blank indica que o campo nao é obrigatorio
    
    slug = models.SlugField('Atalho')
    
    data_inicio =  models.DateField('Data de inicio',null= True,blank=True)
    image = models.ImageField(upload_to='cursos/imagens',verbose_name='imagem',null=True,blank=True)

    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    #cria uma chave estrangeira para associar usuario ao curso
    user = models.ForeignKey(User,on_delete=models.PROTECT)

    def __str__(self) -> str: # define um nome para o objeto
        return self.nome
    
    class Meta:

        verbose_name = 'Curso'
        verbose_name_plural ='Cursos'
    