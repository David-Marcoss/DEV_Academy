from dataclasses import fields
from email.mime import image
import http
from http.client import HTTPResponse
from multiprocessing import context
from pyexpat import model
from re import template
from tokenize import group
from urllib import request
from django.views.generic import UpdateView,ListView,CreateView,DeleteView
from .models import modelcursos,matricula,aulas_curso,modulo_curso
from .forms import contatocurso,criar_moduloform

from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from slug import slug
import random
from django.contrib.auth.decorators import login_required

"""
este é uma app padrao do django que serve para enviar mensagens para os templates
para indicar que alguma ação foi realizada
"""
from django.contrib import messages

"""
serve para apenas permitir acesso a view se o usuario for pertencente ao grupo predefinio
para ter acesso a view
"""
from braces.views import GroupRequiredMixin


#serve para apenas permitir acesso a view se o user estiver logado
from django.contrib.auth.decorators import login_required                     

from accounts.models import User

# Create your views here.

class cursosview(ListView):

    model = modelcursos
    template_name = 'cursos/cursos.html'

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Listagem de Cursos do DEV Academy'


        return context

@login_required
def detalhes_cursoview(request,slug):
    context = {}
    
    course = get_object_or_404(modelcursos, slug=slug) #função busca um elemento de uma tabela
    criador = get_object_or_404(User, username = course.user)
    matriculado = matricula.objects.filter(user = request.user,curso = course).exists()
    
    form = contatocurso(request.POST or None) #request.POST retorna um discionario com os atributos enviados do formulario

    if form.is_valid():
        context['is_valid'] = True
        
        form.enviar_email(course,criador.email)
        form = contatocurso()

    context['matriculado'] = matriculado
    context['course'] =  course #contexto serve para passar um objeto para um template
    context['form'] =  form
    context['criador'] =  criador  

    template_name = 'cursos/detalhes_curso.html'
    
    return render(request, template_name, context)


class CadastroCursoview(GroupRequiredMixin,CreateView):
    
    group_required = u'professor'
    model = modelcursos
    """
    utilizando o CreateView não é nescessario criar um formulario para o model
    pois ele ja cria o formulario automaticamente com base nas fields definidas
    form = cadastrocurso
    
    """
    fields = ['nome','descricao','sobre_curso','data_inicio','image','categoria']
    
    template_name = 'form.html'

    success_url= reverse_lazy('cursos')

    """
    for_valid serve para rescrever função de validação do CreateView, para isso basta
    passar o form do createview, para acessar atributos do form usa: form.instance.atributo
    e para salvar form utiliza o metodo return super().form_valid(form)
    
    """ 



    def form_valid(self, form):

        slug_curso = slug(form.instance.nome) + '-' + self.request.user.username +'-'+ f'{random.randint(0,1000)}'

        form.instance.slug = slug_curso
        form.instance.user = self.request.user

        form.save()

        return super().form_valid(form)

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Criar Curso'
        context['botao'] = 'Criar'

        return context
        

class Edit_cursoview(LoginRequiredMixin,UpdateView):
    
    login_url = reverse_lazy('login')
    template_name = 'form.html'
    model = modelcursos
    fields = ['nome','descricao','sobre_curso','image']

    success_url = reverse_lazy('cursos')
    
    def get_object(self, queryset = None):

        object = get_object_or_404(modelcursos,pk = self.kwargs['pk'],user = self.request.user)
        
        return object

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Editar Curso'
        context['botao'] = 'Salvar Alterações'


        return context

#metodo responsavel por realizar matricula do usuario no curso
@login_required
def matriculaview(request,slug):
    
    curso = get_object_or_404(modelcursos, slug=slug)

    """
    objects.get_or_create serve para retornar um objeto caso ele exista no model
    ou inserir o objeto no model se nao existir 
    """
    inscricao,success = matricula.objects.get_or_create(user = request.user,curso = curso)

    messages.info(request,'Inscrição realizada com sucesso!!')
      

    return redirect('meus-cursos-matriculados')

#este metodo cancela a matricula do user no curso
@login_required
def Cancelar_matriculaview(request,pk):
    
    curso = get_object_or_404(modelcursos,id = pk)
    object = get_object_or_404(matricula,curso = curso, user = request.user)

    object.delete()
    
    messages.info(request,'Inscrição Cancelada!!')

    return redirect('meus-cursos-matriculados')



#mostar os cursos em que o usuario esta matriculado
class Meus_cursos_matriculados_view(LoginRequiredMixin,ListView):

    template_name = "cursos/cursos.html"    
    login_url = reverse_lazy('login')
    model = modelcursos

    #get_queryset serve para perlonalizar os objetos buscado no listView
    def get_queryset(self, queryset = None):

        matriculas = matricula.objects.filter(user = self.request.user)
        cursos = []
        for i in matriculas:
            cursos.append(i.curso)

        self.object_list = cursos

        return self.object_list

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Cursos em que você está matriculado'


        return context


#mostar os cursos criados pelo usuario
class Meus_cursos_criados_view(GroupRequiredMixin,ListView):
    
    group_required = u'professor'
    template_name = "cursos/cursos.html"    
    model = modelcursos

    #get_queryset serve para perlonalizar os objetos buscado no listView
    def get_queryset(self, queryset = None):

        self.object_list = self.request.user.modelcursos_set.all()

        return self.object_list

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Cursos criados'


        return context

def aulaview(request):
    template_name = 'cursos/aula.html'
    
    aula = '''<iframe width="560" height="315" src="https://www.youtube.com/embed/fzqbreu4RwM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
    
    context = {'aula': aula}

    return render(request,template_name,context)

def criar_modulo_cursoView(request,slug):

    template_name = 'form.html'
    model = modulo_curso
    form = criar_moduloform(request.POST or None)

    curso = get_object_or_404(modelcursos,slug = slug,user = request.user)

    
    if form.is_valid():
        form.instance.curso = curso
        form.save()
        
        messages.info(request,'Modulo Criado com Sucesso!!')
        
        return redirect('meus-cursos-criados')
        
    
    context = {'form': form,'titulo':'Criar Modulo do Curso','botao':'Criar'}

    return render(request,template_name,context)

    

