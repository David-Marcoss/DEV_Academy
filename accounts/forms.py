<<<<<<< Updated upstream
=======
from cgitb import reset
>>>>>>> Stashed changes
import email
from multiprocessing import context
from re import template
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import UserCreationForm
<<<<<<< Updated upstream
from django.contrib.auth.models import User
=======

#from accounts.models import User
from django.contrib.auth import get_user_model
>>>>>>> Stashed changes

from django import forms

from .models import redefinir_senha

from paginas.funcoes_auxiliares import generate_hash_key
from paginas.mail import send_mail_template



#para personalizar formularios cria-se uma arquivo form para sobrescreber ou criar formularios
#este arquivo vai servir para personalizar o user padrao do django

<<<<<<< Updated upstream
class Userform(UserCreationForm):
=======
User = get_user_model() 

class UserChangeForm(auth_forms.UserChangeForm):
>>>>>>> Stashed changes

    #campos adicionados ao form user
    email = forms.EmailField(max_length=100)
    tipo_user = forms.ChoiceField(choices = (('1','aluno'),('2','professor')),label='Tipo de Usuário')

    #definição de valores padrao
    class Meta:
<<<<<<< Updated upstream
        model= User  #model padrao de usuarios do django
        fields = ['username','email','tipo_user']
    
    """ 
        Clem_nome_do_campo é metodo padrao do UserCreationForm  para validar campo do form 
        esta função sobreescreve o metodo de validação para que o email seja unico 
    """
    
=======
        model = User  # model padrao de usuarios do django
        fields = ['username', 'email', 'first_name', 'last_name']


class UserCreationForm(auth_forms.UserCreationForm):
    
    tipo_user = forms.ChoiceField(
        choices=(('1', 'aluno'), ('2', 'professor')), label='Tipo de Usuário')

    #definição de valores padrao
    class Meta:
        model = User  # model padrao de usuarios do django
        fields = ['username', 'nome','email', 'tipo_user','imageperfil']



"""
    Form para redefinição de senha, onde o usuario
    deve digitar seu e-mail para recuperar senha
"""
class Redefinir_senhaForm(forms.Form):

    email = forms.EmailField(label='E-mail')


>>>>>>> Stashed changes
    def clean_email(self):

        email = self.cleaned_data['email']

<<<<<<< Updated upstream
        #User.objects.filter(email = email ).exists retorna se o valor passado existe no model
        
        if User.objects.filter(email = email ).exists():
            raise forms.ValidationError('E-mail já cadastrado, insira um novo E-mail')

            #raise retorna uma msg de erro
        
        return email
    
    
    """ 
        metodo padrao do UserCreationForm  para salvar informações do form
        esta função sobreescreve o metodo para que o email seja obrigatorio
    """
    def save(self, commit = True):
        user = super(Userform,self).save(commit=False)
        user.email = self.cleaned_data['email']
=======
        if User.objects.filter(email = email).exists():
            return email
        else:
            raise forms.ValidationError('E-mail não cadastrado!!') 

    def save(self):

        usuario = User.objects.get(email=self.cleaned_data['email'])    
        key = generate_hash_key(usuario.username)

        reset = redefinir_senha(User = usuario,key = key)
        reset.save()

        template_name = 'account/reset_password.html'
        assunto = "Instruções para redefinir senha"
        context = {'reset':reset}

        send_mail_template(assunto,template_name,context,[usuario.email])

>>>>>>> Stashed changes


<<<<<<< Updated upstream
        return user



class EditUserform(UserCreationForm):

    #campos adicionados ao form user
    email = forms.EmailField(max_length=100)
    tipo_user = forms.ChoiceField(choices = (('1','aluno'),('2','professor')),label='Tipo de Usuário')

    #definição de valores padrao
    class Meta:
        model= User  #model padrao de usuarios do django
        fields = ['username','email','first_name','last_name']
            



=======
     
>>>>>>> Stashed changes
