from cgitb import reset
import email
from multiprocessing import context
from re import template
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm

#from accounts.models import User
from django.contrib.auth import get_user_model

from django import forms

from .models import redefinir_senha

from paginas.funcoes_auxiliares import generate_hash_key,acesentar_tempo
from paginas.mail import send_mail_template



#para personalizar formularios cria-se uma arquivo form para sobrescreber ou criar formularios
#este arquivo vai servir para personalizar o user padrao do django

User = get_user_model() 

class UserChangeForm(auth_forms.UserChangeForm):

    #definição de valores padrao
    class Meta:
        model = User  # model padrao de usuarios do django
        fields = ['username', 'nome','email','imageperfil','bio']


#form para cadastro de usuario
class UserCreationForm(auth_forms.UserCreationForm):
    
    tipo_user = forms.ChoiceField(
        choices=(('1', 'aluno'), ('2', 'professor')), label='Tipo de Usuário')

    #definição de valores padrao
    class Meta:
        model = User  # model padrao de usuarios do django
        fields = ['username', 'nome','email', 'tipo_user','imageperfil','bio']



"""
    Form para redefinição de senha, onde o usuario
    deve digitar seu e-mail para recuperar senha
"""
class Redefinir_senhaForm(forms.Form):

    email = forms.EmailField(label='E-mail')


    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email = email).exists():
            return email
        else:
            raise forms.ValidationError('E-mail não cadastrado!!') 

    def save(self):

        usuario = User.objects.get(email=self.cleaned_data['email'])    
        key = generate_hash_key(usuario.username)

        reset = redefinir_senha(User = usuario,key = key) 
        #salva os dados no banco e armazena o horario em que a key foi gerada
        reset.save()

        #define o tempo em que a key é valida que de 1h
        time = acesentar_tempo(reset.horario)
        reset.expira_em = time 

        reset.save()
        

        template_name = 'account/reset_password.html'
        assunto = "Instruções para redefinir senha"
        context = {'reset':reset}

        send_mail_template(assunto,template_name,context,[usuario.email])



     