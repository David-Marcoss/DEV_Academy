from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class modelaluno(models.Model):
    nome = models.CharField('Nome completo',max_length=100,null=True)
    imageperfil = models.ImageField(upload_to='perfil/imagens',verbose_name='imagem perfil',null=True,blank=True)
    #cria uma relação de um para um
    perfil = models.OneToOneField(User,on_delete=models.CASCADE)
    #on_delete = on_delete=models.CASCADE siginifica que se for deletado o user tambem é deletado o aluno

    def __str__(self):
        return self.nome
    
    class meta:
        verbose_name = 'Perfil Aluno'
        verbose_name_plural ='Perfil Alunos'

class modelprofessor(modelaluno):
    qualificacao = models.TextField('Qualificação',max_length=200,null=True)

    class meta:
        verbose_name = 'Perfil Professor'
        verbose_name_plural ='Perfil Professores'
