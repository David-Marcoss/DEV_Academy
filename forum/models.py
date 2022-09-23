from django.db import models
from accounts.models import User
from cursos.models import modelcursos
from paginas.mail import send_mail_template

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

    topico = models.ForeignKey(Topicos,on_delete=models.CASCADE,related_name='respostas')
    autor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='autor_r')

    criado_em= models.DateTimeField('criado em: ',auto_now_add=True)
    atualizado_em= models.DateTimeField('atualizado em: ',auto_now=True)

    def __str__(self) -> str: # define um nome para o objeto
        return 'Respostas do ' + self.topico.titulo
    
    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['criado_em']
"""
Esta função serve para que ela seja disparada por um sinal 
toda vez que for salvo um aviso no model avisos é disparado esta
função que ira ser responsavel por enviar o aviso cadastrado aos
alunos que estao matriculados no curso
"""

def enviar_resposta_topico_email(instance, created, **kwargs):
    topico = instance.topico
    if created and topico.notificacoes and topico.autor != instance.autor:

        template_name = 'cursos/forum/resposta_topico_email.html'
        assunto = f"{instance.autor} respondeu seu Topico {topico.titulo}:"
        context = {'topico':topico,'resposta':instance}

        send_mail_template(assunto,template_name,context,[topico.autor.email])

#metodo responsavel por disparar o sinal para execultar a função acima
models.signals.post_save.connect(enviar_resposta_topico_email,sender = Respostas, dispatch_uid = 'enviar_aviso_email') 


class like(models.Model):

    resposta = models.ForeignKey(Respostas,on_delete=models.CASCADE,related_name='like_r')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='like')

    def __str__(self) -> str: # define um nome para o objeto
        return self.user + ' like ' + self.resposta
        
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'



