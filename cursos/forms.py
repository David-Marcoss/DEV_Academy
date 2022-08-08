from dataclasses import fields
import email

from django.conf import settings
from django import forms

from django.core.mail import send_mail
from paginas.mail import send_mail_template

from .views import modelcursos

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

"""
class cadastrocurso(forms.Form):

    nome = forms.CharField(max_length=100,label='Titulo do curso')
    descricao = forms.CharField(max_length=200,label='descrição breve',required=True) #blank indica que o campo nao é obrigatorio
    
    sobre_curso = forms.CharField(label='sobre o curso',required=True,widget=forms.Textarea) #blank indica que o campo nao é obrigatorio
    
    data_inicio =  forms.DateField(label='Data de inicio',required=True)
    image = forms.ImageField(label='imagem',allow_empty_file=False)
    slug = forms.SlugField(label='slug')

"""

"""
foma simplificade de criar form, utulizando model form
class cadastrocurso(forms.ModelForm):

    class meta:
        model = modelcursos
        fields = fields = ['nome','descricao','sobre_curso','data_inicio','image']

 """   
