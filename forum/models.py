from django.db import models
from accounts.models import User
from cursos.models import modelcursos

# Create your models here.

class Forum(models.Model):
    
    titulo = models.CharField('titulo',max_length=100,blank=True,default=f'Forum do Curso')
    curso = models.OneToOneField(modelcursos,on_delete=models.PROTECT,related_name='forum')

    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    def __str__(self) -> str: # define um nome para o objeto
        return self.titulo
    
    def get_topicos(self):
        return self.topicos.all()

    class Meta:
        verbose_name = 'Forum do curso'
    


class Topicos(models.Model):
    
    titulo = models.CharField('titulo',max_length=100)
    assunto = models.TextField('Assunto')

    notificacoes = models.BooleanField('Deseja receber notificações sobre este Topico?',blank=True,default=False)
    
    num_respostas = models.IntegerField('Numero de respostas',blank=True,default=0)
    visualizacoes = models.IntegerField('Visualisações',blank=True,default=0)

    forum = models.ForeignKey(Forum,on_delete=models.PROTECT,related_name='topicos')
    autor = models.ForeignKey(User,on_delete=models.PROTECT,related_name='autor_t')


    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    def __str__(self) -> str: # define um nome para o objeto
        return self.titulo
    
    def get_respostas(self):
        return self.respostas.all()
    
    
    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-atualizado_em']


class Respostas(models.Model):
    resposta = models.TextField('Resposta')
    like = models.IntegerField("Numero de Likes",blank=True,default=0)

    topico = models.ForeignKey(Topicos,on_delete=models.PROTECT,related_name='respostas')
    autor = models.ForeignKey(User,on_delete=models.PROTECT,related_name='autor_r')

    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    def __str__(self) -> str: # define um nome para o objeto
        return 'Respostas do ' + self.topico.titulo
    
    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['atualizado_em']



