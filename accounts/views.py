from cgitb import reset
import email
from multiprocessing import context
from pipes import Template
from re import template
import re
from typing_extensions import Self
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect

from django.views.generic import CreateView,TemplateView,UpdateView

# o django por padrao ja possui um model e um form para cadastro de usuarios
<<<<<<< Updated upstream
from django.contrib.auth.forms import PasswordChangeForm  #form padrao para alteração de senha
from django.contrib.auth.models import User             #model padrao de cadastro de usuario
=======
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm  #form padrao para alteração de senha
from accounts.models import User
>>>>>>> Stashed changes

from django.contrib.auth import authenticate,login #metodos de login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User

from django.conf import settings
from DMS_cursos.settings import LOGIN_REDIRECT_URL

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from cursos.models import modelcursos

<<<<<<< Updated upstream
from .forms import Userform,EditUserform
=======
from .forms import UserChangeForm, UserCreationForm,Redefinir_senhaForm
>>>>>>> Stashed changes

from .models import modelaluno,modelprofessor,redefinir_senha

from paginas.funcoes_auxiliares import generate_hash_key


"""
request é outra forma de renderizar um template e manipular o template
para isso ele precisa de um tamplate_name para indicar qual template sera
renderizado, context que é um discionario para passar variaveis para o template
e para renderizar template retorne utilizando a função render (request,template_name,context)

para receber informações de um form utilizando o request primeiramente voce deve
verificar o meto do do form que geralmente é post, e para pegar os volores do form
utiliza-se request.POST, apos isso voce pode utilizar as funcionalidade do form para
manipular os dados do form


"""
def cadastroview(request):

    template_name = "cadastro.html"

    if request.method == 'POST': # verifica se o meto de formulario é post
        
        form = Userform(request.POST) #requeste armazena os dados preencidos pelo ususario

        if form.is_valid(): #verifica se o formulario é valido

            
            user = form.save() # salva os dados do form no banco

            #vrifica qual é o tipo de usuario
            if form.cleaned_data['tipo_user'] == '1':
                grupo = get_object_or_404(Group,name='aluno')
                #cria perfil do user
                modelaluno.objects.create(perfil = user)
            
            else:
                grupo = get_object_or_404(Group,name='professor')
                modelprofessor.objects.create(perfil = user)
                print("professor")
            
            #salva usuario ao grupo espesifico
            user.groups.add(grupo)

            
            user = authenticate(username = user.username,password = form.cleaned_data['password1'])
            
            login(request,user)

            return redirect('home')
    
    
    else:
        form = Userform()


    context = { 'form':  form ,'titulo': 'Criar Conta','submit' : 'Cadastrar-se'}

    return render(request,template_name,context)


def redefinir_senhaview(request):
    
    """form recebe o request.POST com os dados preenchidos do formulario se o form
       foi preenchido ou recebe None se o form ainda não foi preenchido
    """
    template_name = 'account/redefinir_senha.html'
    success = False

    form = Redefinir_senhaForm(request.POST or None)  

    if form.is_valid():

        form.save()

        #indica se a operação ocorreu com sucesso
        success = True


    else:
        form = Redefinir_senhaForm()

    context['success'] = success
    context['form'] = form
    context['titulo'] = 'Digite seu E-mail para redefinir senha'
    context['botao'] = 'Submeter'
    context['success_msg'] = 'E-mail confirmado com sucesso!!Foi enviado um E-mail para você com mais detalhes para redefinir sua senha'

    return render(request,template_name,context)


    return render(request,template_name,context)


def reset_passwordview(request,key):

    template_name = 'account/redefinir_senha.html'
    context = {}

    success = False

    reset = get_object_or_404(redefinir_senha,key=key)

    form = SetPasswordForm(user = reset.User,data = request.POST or None)

    if form.is_valid():

        reset.confirmado = True
        reset.save()

        form.save()

        success = True
    
    context['success'] = success
    context['form'] = form
    context['titulo'] = 'Redefinir senha'
    context['botao'] = 'Confirmar'
    context['success_msg'] = 'Senha redefinida com sucesso!!'

    return render(request,template_name,context)



@login_required
def perfilview(request):

    template_name = "profile.html"
    user = request.user
    cursos = ''
    tipo_user = ''
    
    """
        é possivel acessar os cursos que estao relacionados a um usuario atravez 
        do comando nome_do_atributo.nome_do_model_relacionado_set (EX:user.modelcursos_set )
        com esse comando é retornado todos os dados que estao relacionados ao atributo
    
    """
    
    if user.is_Teacher:
        tipo_user = 'Professor'
        cursos = user.modelcursos_set.all()
    else:
        tipo_user = 'Aluno'

    context = {'cursos': cursos,'tipo_user':tipo_user}

    return render(request,template_name,context)



"""
função pendente implementar atualização dados do perfil 

class Updateperfilview(UpdateView):
 
    user = self.request.user
    template_name = 'editperfil.html'
    
    if user.groups.filter(name='professor').exists():
        pass
    else:
        pass
    
    def get_object(self, queryset= None):
        return super().get_object(queryset)

"""

class UserUpdate(UpdateView):
    model= User
    template_name = 'form.html'

    fields = ['username','email','nome','imageperfil']

    success_url = reverse_lazy('perfil') 

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Editar Perfil'
        context['botao'] = 'Salvar Alterações'

        return context


@login_required
def UserpasswordUpdate(request):
    
    template_name = 'form.html'
    form = PasswordChangeForm(user=request.user)
    
    if request.method == 'POST':
        form = PasswordChangeForm(data= request.POST, user=request.user)

        if form.is_valid():
            form.save()
    

    context = {'form' : form,'titulo':'Editar Senha','botao':'Salvar Alterações'}

    return render(request,template_name,context)




"""
CreateView serve para renderizar formulario e cadastrar os dados do 
formulario digitado pelo ususario para isso esta função necessita do
nome do template que ira receber o form, o model que ira armazenar os
dados uma lista de filds que é os campos do model que ira aparecer no form
e success_url que é a url que o usuario vai ser redirecionado apos concluir 
o cadastro.

"""
