import email

from django.conf import settings
from django import forms

from django.core.mail import send_mail
from paginas.mail import send_mail_template

class contatocurso(forms.Form):

    nome = forms.CharField(label='Nome',max_length=100)
    email = forms.EmailField(label='Email')
    menssagem = forms.CharField(label='Mensagem',widget=forms.Textarea)

    def enviar_email(self,curso):
       subject = f'Contato: {curso}'
       context = {
            'name': self.cleaned_data['nome'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['menssagem'],
       }
        
       template_name = 'contact_email.html'
        
       send_mail_template(subject, template_name, context, [settings.CONTACT_EMAIL])