import email
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

#para personalizar formularios cria-se uma arquivo form para sobrescreber ou criar formularios
#este arquivo vai servir para personalizar o user padrao do django

class Userform(UserCreationForm):

    #campos adicionados ao form user
    email = forms.EmailField(max_length=100)
    tipo_user = forms.ChoiceField(choices = (('1','aluno'),('2','professor')),label='Tipo de Usuário')

    #definição de valores padrao
    class Meta:
        model= User  #model padrao de usuarios do django
        fields = ['username','email','tipo_user']
    
    """ 
        Clem_nome_do_campo é metodo padrao do UserCreationForm  para validar campo do form 
        esta função sobreescreve o metodo de validação para que o email seja unico 
    """
    
    def clean_email(self):
        email = self.cleaned_data['email']

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

        if commit:
            user.save()

        return user



class EditUserform(UserCreationForm):

    #campos adicionados ao form user
    email = forms.EmailField(max_length=100)
    tipo_user = forms.ChoiceField(choices = (('1','aluno'),('2','professor')),label='Tipo de Usuário')

    #definição de valores padrao
    class Meta:
        model= User  #model padrao de usuarios do django
        fields = ['username','email','first_name','last_name']
            



