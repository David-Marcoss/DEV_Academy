from multiprocessing import context
from pipes import Template
from django.forms import PasswordInput
from django.shortcuts import render, redirect

from django.views.generic import CreateView,TemplateView

# o django por padrao ja possui um model e um form para cadastro de usuarios
from django.contrib.auth.forms import UserCreationForm  #form padrao de cadastro de usuario
from django.contrib.auth.models import User             #model padrao de cadastro de usuario

from django.contrib.auth import authenticate,login #metodos de login
from django.contrib.auth.decorators import login_required 

from django.conf import settings
from DMS_cursos.settings import LOGIN_REDIRECT_URL

from django.urls import reverse_lazy

from .forms import Userform


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

    template_name = "form.html"

    if request.method == 'POST': # verifica se o meto de formulario é post
        
        form = Userform(request.POST) #requeste armazena os dados preencidos pelo ususario

        if form.is_valid(): #verifica se o formulario é valido
            
            user = form.save() # salva os dados do form no banco
            
            user = authenticate(username = user.username,password = form.cleaned_data['password1'])
            login(request,user)

            return redirect('home')
    
    
    else:
        form = Userform()


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

    return render(request,template_name)












