from multiprocessing import context
from pipes import Template
from re import template
from typing_extensions import Self
from unicodedata import name
from urllib import request
from django.shortcuts import render, redirect

from django.views.generic import CreateView,TemplateView,UpdateView

# o django por padrao ja possui um model e um form para cadastro de usuarios
from django.contrib.auth.forms import PasswordChangeForm  #form padrao para alteração de senha
from accounts.models import User

from django.contrib.auth import authenticate,login #metodos de login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.conf import settings
from DMS_cursos.settings import LOGIN_REDIRECT_URL

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from cursos.models import modelcursos

from .forms import UserChangeForm, UserCreationForm

from .models import modelaluno,modelprofessor


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
        
        # requeste armazena os dados preencidos pelo ususario
        form = UserCreationForm(request.POST)

        if form.is_valid(): #verifica se o formulario é valido

            user = form.save(commit=False) # salva os dados do form no banco

            #vrifica qual é o tipo de usuario
            if form.cleaned_data['tipo_user'] == '1':
                grupo = get_object_or_404(Group,name='aluno')
                
                user.is_Teacher = False
                user = form.save()  # salva os dados do form no banco

                #cria perfil do user
                modelaluno.objects.create(
                    perfil = user,
                    nome = "Teste"
                )

            else:
                grupo = get_object_or_404(Group,name='professor')

                user.is_Teacher = True
                user = form.save()  # salva os dados do form no banco

                modelprofessor.objects.create(
                    perfil = user,
                    nome="Teste",
                )

            #salva usuario ao grupo espesifico
            user.groups.add(grupo)

            
            user = authenticate(username = user.username,password = form.cleaned_data['password1'])
            
            login(request,user)

            return redirect('home')
    
    
    else:
        form = UserCreationForm()


    context = { 'form':  form ,'titulo': 'Criar Conta','submit' : 'Cadastrar-se'}

    return render(request,template_name,context)


"""
CreateView serve para renderizar formulario e cadastrar os dados do 
formulario digitado pelo ususario para isso esta função necessita do
nome do template que ira receber o form, o model que ira armazenar os
dados uma lista de filds que é os campos do model que ira aparecer no form
e success_url que é a url que o usuario vai ser redirecionado apos concluir 
o cadastro.

"""

"""
OUTRA FORMA DE CADASTRO DE USUSARIO

class cadastroview2(CreateView):
    
    template_name= 'form.html'
    
    form_class= Userform
    success_url= reverse_lazy('home')


    #get_context_data serve para passar valores para o template 
    def get_context_data(self, *args,**kwargs):
        
        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Criar Conta'
        context['submit'] = 'Cadastrar-se'

        return context



"""

@login_required
def perfilview(request):

    template_name = "profile.html"
    user = request.user
    
    cursos = ''
    tipo_user = ''

    if user.groups.filter(name='professor').exists():

        tipo_user = 'Professor'
        
        if modelcursos.objects.filter(user = user.id).exists():
            cursos = modelcursos.objects.filter(user = user.id)
        else:
            cursos = None
    
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

    fields = ['username','email','first_name','last_name']

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




