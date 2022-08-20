from cProfile import label
from cgitb import reset
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

from DMS_cursos.settings import AUTH_USER_MODEL

# Create your models here.


class User(AbstractUser):
    
    nome = models.CharField('Nome completo',max_length=100,null=True,blank=True)
    imageperfil = models.ImageField(upload_to='perfil/imagens',verbose_name='imagem perfil',null=True,blank=True)
    is_Teacher = models.BooleanField(default=False)
    email = models.EmailField('E-mail',blank=False,unique=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "usuario"

    def __str__(self):
        return f"{self.username}"


"""
    Este model serve para auxiliar na recuperação de senhas do usuario
    e armazenar o historico de auterações de senha ele aramzenha o ususario
    que esta tenteando alterar senha, uma chave unica string para gerar um link
    para que o usuario possa alterar senha e a data da criação da geração da chave
    e se uma confirmação para que seja indicado se a senha foi ou nao alterada 

"""
class redefinir_senha(models.Model):

    User = models.ForeignKey(AUTH_USER_MODEL,verbose_name='Usuario', related_name='resets',on_delete=models.PROTECT)
    key = models.TextField('key',max_length=100,unique=True)
    criado_em = models.DateField('Data criação',auto_now=True)
    confirmado = models.BooleanField('Senha foi redefinida:',default=False)
    horario = models.TimeField('horario de criação',auto_now=True)
    expira_em = models.TimeField('tempo para expirar',null=True)

    def __str__(self):
        return f"{self.User} {self.criado_em}"
    
    class meta:
        verbose_name = 'Nova senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-criado_em']



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
