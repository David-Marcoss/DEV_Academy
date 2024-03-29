from dataclasses import fields
import email
from pyexpat import model

from django.conf import settings
from django import forms
from paginas.mail import send_mail_template

from .models import modelcursos, modulo_curso,aulas_curso,avisos_curso,materiais_curso
from .funcoes_auxiliares import trata_link,verifica_link

#form para entrar em contato com o criador do curso
class contatocurso(forms.Form):

    nome = forms.CharField(label='Nome',max_length=100)
    email = forms.EmailField(label='Email')
    menssagem = forms.CharField(label='Mensagem',widget=forms.Textarea)

    def enviar_email(self,curso,email_criador):
       subject = f'Contato: {curso}'
       context = {
            'name': self.cleaned_data['nome'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['menssagem'],
       }
        
       template_name = 'cursos/contact_email.html'
        
       send_mail_template(subject, template_name, context, [email_criador])
   

class criar_moduloform(forms.ModelForm):
     
     class Meta:
          model = modulo_curso
          fields = ['titulo']

class criar_aula_moduloform(forms.ModelForm):
     
     class Meta:
          model = aulas_curso
          fields = ['titulo','video','sobre_aula']
     
     #função para validação do campo video
     def clean_video(self):
          
          if verifica_link(self.cleaned_data['video']):
               video = self.cleaned_data['video']
               video = trata_link(video)
               
               return video
          else:
               raise forms.ValidationError('Por favor, digite um link valido!!') 


class avisos_cursoform(forms.ModelForm):
     
     class Meta:
          model = avisos_curso
          fields = ['titulo','assunto']

class material_cursoform(forms.ModelForm):
     
     class Meta:
          model = materiais_curso
          fields = ['titulo','material']

class edit_curso_dash(forms.ModelForm):
     class Meta:
          model = modelcursos
          fields = ['nome','descricao','sobre_curso']

class edit_curso_image_dash(forms.ModelForm):
     class Meta:
          model = modelcursos
          fields = ['image']