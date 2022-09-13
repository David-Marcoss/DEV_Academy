from cgitb import text
from copyreg import dispatch_table
from curses.ascii import NUL
from distutils.command.upload import upload
from distutils.text_file import TextFile
from email.mime import image
from enum import unique
from pickle import TRUE
from pyexpat import model
from tabnanny import verbose
from telnetlib import STATUS
from typing import OrderedDict
from typing_extensions import Self
from unicodedata import name
from django.db import models
from django.forms import CharField


from accounts.models import User
from paginas.mail import send_mail_template

#serve para limitar quais tipos de arquivos sao permitidos no FileFild
from django.core.validators import FileExtensionValidator

#model que armazena as categorias dos cursos
class categoria_curso(models.Model):
    categoria = models.CharField('Categoria do curso',max_length=100)

    def __str__(self) -> str: # define um nome para o objeto
        return self.categoria
    
    class Meta:

        verbose_name = 'Categoria curso'
        verbose_name_plural ='Categorias cursos'


#model que armazena os cursos
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
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='cursos')
    categoria = models.ForeignKey(categoria_curso,on_delete=models.CASCADE)


    def __str__(self) -> str: # define um nome para o objeto
        return self.nome
    
    def get_modulos(self):
        return self.modulo.all()
    
    def get_numero_aulas(self):
        num = 0
        for i in self.get_modulos():
            num += i.aulas.all().count()
        
        return num
    
    def get_num_alunos_matriculados(self):
        return self.matricula.all().count()
    
    def get_materiais_curso(self):
        return self.materiais.all()
    
    class Meta:

        verbose_name = 'Curso'
        verbose_name_plural ='Cursos'


#model que armazena os modulos do curso
class modulo_curso(models.Model):

    titulo = models.CharField('Titulo do modulo',max_length=100)
    #status == False indica que o modulo ainda não foi finalizado e True o modulo ja foi finalizado
    status_modulo = models.BooleanField('Status do modulo:',default=False)
    
    numero_modulo = models.IntegerField('numero aula',blank=True,default=0)
    
    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    curso = models.ForeignKey(modelcursos,on_delete=models.PROTECT,related_name='modulo')
    

    def __str__(self) -> str: # define um nome para o objeto
        return self.titulo
    
    def get_aulas(self):
        return self.aulas.all()
    
    class Meta:

        verbose_name = 'Modulo'
        verbose_name_plural ='Modulos'


#model que armazena os modulos do curso
class aulas_curso(models.Model):

    titulo = models.CharField('Titulo da Aula',max_length=100)
    
    video = models.CharField('link do Video',max_length=100,blank=False)
    
    sobre_aula = models.TextField('sobre a aula',blank=True,null=True)

    numero_aula = models.IntegerField('numero aula',blank=True,default=0)

    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    modulo = models.ForeignKey(modulo_curso,on_delete=models.PROTECT,related_name='aulas')
    

    def __str__(self) -> str: # define um nome para o objeto
        return self.titulo
    
    class Meta:

        verbose_name = 'Aula curso'
        verbose_name_plural ='Aulas cursos'

class materiais_curso(models.Model):
    titulo = models.CharField('Titulo do material',max_length=100)
    
    material = models.FileField(upload_to='cursos/materiais',verbose_name='Material'
    ,validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx','txt','pptx'])])

    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    curso = models.ForeignKey(modelcursos,on_delete=models.PROTECT,related_name='materiais')
    

    def __str__(self) -> str: # define um nome para o objeto
        return self.titulo
    
    class Meta:

        verbose_name = 'Materiais do curso'


#model que armazena as matriculas dos cursos
class matricula(models.Model):

    data_matricula = models.DateTimeField('criado em: ',auto_now_add=True)
    curso = models.ForeignKey(modelcursos,on_delete=models.CASCADE,related_name='matricula')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='matricula')

    notificacoes = models.BooleanField('deseja receber notificações do curso',blank=True,default=True)

    def __str__(self) -> str: # define um nome para o objeto
        return f'{self.user} matriculado em {self.curso}'
    
    class Meta:

        verbose_name = 'Matricula'
        verbose_name_plural ='Matriculas'
        #esta variavel serve para definir um unico objeto entre o usuario e o curso
        unique_together = (('user','curso')) 


#model reponsavel por armazenar avisos do curso
class avisos_curso(models.Model):

    titulo = models.CharField('Titulo',max_length=100)
    assunto = models.TextField('Assunto')
    
    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    curso = models.ForeignKey(modelcursos,on_delete=models.PROTECT,related_name='avisos')

    
    def __str__(self) -> str: # define um nome para o objeto
        return self.titulo
    
    class Meta:

        verbose_name = 'Aviso'
        verbose_name_plural ='Avisos'
        ordering = ['-criado_em']


"""
Esta função serve para que ela seja disparada por um sinal 
toda vez que for salvo um aviso no model avisos é disparado esta
função que ira ser responsavel por enviar o aviso cadastrado aos
alunos que estao matriculados no curso
"""
def enviar_aviso_email(instance, created, **kwargs):
    if created:
        template_name = 'cursos/aviso_curso_email.html'
        assunto = instance.titulo
        context = {'aviso':instance}

        matriculas = matricula.objects.filter(curso = instance.curso)

        for i in matriculas:
            if i.notificacoes:
                send_mail_template(assunto,template_name,context,[i.user.email])

#metodo responsavel por disparar o sinal para execultar a função acima
models.signals.post_save.connect(enviar_aviso_email,sender = avisos_curso, dispatch_uid = 'enviar_aviso_email') 

    
