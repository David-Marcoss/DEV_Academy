from dataclasses import fields
from email.mime import image
import http
from http.client import HTTPResponse
from multiprocessing import context
from pipes import Template
from pyexpat import model
from re import template
from tokenize import group
from urllib import request
from django.views.generic import UpdateView,ListView,CreateView,DeleteView

from .models import *
from .forms import *

from django import forms

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
from django import forms

"""
serve para apenas permitir acesso a view se o usuario for pertencente ao grupo predefinio
para ter acesso a view
"""
from braces.views import GroupRequiredMixin


#serve para apenas permitir acesso a view se o user estiver logado
from django.contrib.auth.decorators import login_required                     

from accounts.models import User

from .decorator import is_creator,matriculado

# Create your views here.


class DateInput(forms.DateInput):
    input_type = 'date'

class cursosview(ListView):

    model = modelcursos
    template_name = 'cursos/cursos.html'

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Listagem de Cursos do DEV Academy'


        return context

# @login_required
def detalhes_cursoview(request,slug):
    context = {}
    
    course = get_object_or_404(modelcursos, slug=slug) #função busca um elemento de uma tabela
    criador = get_object_or_404(User, username = course.user)
    
    if str(request.user) != "AnonymousUser":
        matriculado = matricula.objects.filter(user = request.user,curso = course).exists()
    else:
        matriculado = None
    
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

    def get_form(self, form_class=None):
        form = super(CadastroCursoview, self).get_form(form_class)
        form.fields['data_inicio'].widget = DateInput()
        return form

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
    
    #redireciona a pagina anterior que solicitou a edição
    def get_success_url(self):
        messages.info(self.request,'Alterações salvas com sucesso!!')
        return self.request.GET.get('next', reverse_lazy('meus-cursos-criados'))


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
      
    #redireciona para pagina que solicitou a operação
    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))

#este metodo cancela a matricula do user no curso
@login_required
def Cancelar_matriculaview(request,pk):
    
    curso = get_object_or_404(modelcursos,id = pk)
    object = get_object_or_404(matricula,curso = curso, user = request.user)

    object.delete()
    
    messages.info(request,'Inscrição Cancelada!!')

    #redireciona para pagina que solicitou a operação
    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))



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

"""
faz o cadastro de um modulo no curso somente o usuario que criou
o curso pode realizar esta operação
"""
@login_required
@is_creator
def cadastrar_modulo_cursoView(request,slug):

    template_name = 'cursos/dashboard/form.html'
    form = criar_moduloform(request.POST or None)

    curso = request.curso

    if form.is_valid():
        form.instance.curso = curso
        form.instance.numero_modulo = curso.modulo.all().count() + 1
        form.save()
        
        messages.info(request,'Modulo Criado com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-criados')))
        
    context = {'form': form, 'curso': curso, 'titulo': 'Cadastrar Modulo do Curso', 'botao': 'Cadastrar'}

    return render(request,template_name,context)

# view responsavel por mostrar lista de modulos do curso
class ver_modulos_cursoView(GroupRequiredMixin,ListView):
    
    group_required = u'professor'
    template_name = 'cursos/dashboard/modulos_curso.html'
    model = modulo_curso
    
    def get_queryset(self, queryset = None):

        curso = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)

        self.object_list = curso.modulo.all() 

        return self.object_list
    
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['curso'] = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)

        return context

#View responsavel por editar um modulo do curso
class Edit_moduloView(GroupRequiredMixin,UpdateView):
    
    group_required = u'professor'
    template_name = 'cursos/dashboard/form.html'
    model = modulo_curso
    fields = ['titulo']

    def get_object(self, queryset = None):

       curso = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)
       object = get_object_or_404(modulo_curso,id = self.kwargs['pk'],curso = curso)

       return object

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        curso = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)
        context['curso'] = curso
        context['titulo'] = 'Editar Modulo'
        context['botao'] = 'Salvar Alterações'

        return context
    
    #redireciona a pagina anterior que solicitou a edição
    def get_success_url(self):
        messages.info(self.request,'Alterações salvas com sucesso!!')
        return self.request.GET.get('next', reverse_lazy('meus-cursos-criados'))


"""
este metodo responsavel por excluir modulo do curso, so é possivel
excluir se o modulo não possuir aulas cadastradas
"""
@login_required
@is_creator
def deletar_modulo_cursoView(request,slug,pk):
    modulo = get_object_or_404(modulo_curso,id = pk,curso = request.curso)

    if modulo.aulas.all():
        messages.info(request,'Não é possivel excluir modulo com aulas cadastradas!!')
    else:    
        modulo.delete()
        messages.info(request,'Modulo excluido com sucesso!!')
    

    #redireciona para pagina que solicitou a operação
    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))

    
"""
faz o cadastro de uma aula no modulo no curso somente o usuario que criou
o curso pode realizar esta operação
"""
@login_required
@is_creator
def cadastrar_aula_modulo_cursoView(request,slug,pk):

    template_name = 'cursos/dashboard/form.html'
    form = criar_aula_moduloform(request.POST or None)
    
    modulo = get_object_or_404(modulo_curso,id = pk,curso = request.curso)

    if form.is_valid():
        
        form.instance.modulo = modulo
        form.instance.numero_aula = request.curso.get_numero_aulas() + 1 
        form.save()
        
        messages.info(request,'Aula Criado com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-criados')))
    
    context = {'form': form, 'titulo': 'Cadastrar aula no Modulo',
               'botao': 'Cadastrar', 'curso': request.curso}

    return render(request,template_name,context)

#View responsavel por editar aula do modulo do curso
class Edit_aula_moduloView(GroupRequiredMixin,UpdateView):
    
    group_required = u'professor'
    template_name = 'cursos/dashboard/form.html'
    model = aulas_curso
    form_class= criar_aula_moduloform
    
    def get_object(self, queryset = None):

       curso = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)
       
       object = get_object_or_404(aulas_curso,id = self.kwargs['pk'])
       
       return object

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['curso'] = get_object_or_404(
            modelcursos, slug=self.kwargs['slug'], user=self.request.user)
        context['titulo'] = 'Editar Aula'
        context['botao'] = 'Salvar Alterações'

        return context
    
    #redireciona a pagina anterior que solicitou a edição
    def get_success_url(self):
        messages.info(self.request,'Alterações salvas com sucesso!!')

        return self.request.GET.get('next', reverse_lazy('meus-cursos-criados'))


#view responsavel por mostrar aulas de um modulo
class ver_aulas_modulos_cursoView(GroupRequiredMixin,ListView):
    
    group_required = u'professor'
    template_name = 'cursos/dashboard/aulas_modulo_curso.html'
    model = aulas_curso
    
    def get_queryset(self, queryset = None):

        curso = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)
        modulo = get_object_or_404(modulo_curso,id = self.kwargs['pk'],curso = curso)
 
        return modulo.aulas.all()
    
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['curso'] = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)
        context['modulo'] = get_object_or_404(modulo_curso,id = self.kwargs['pk'])

        return context
    
"""
este metodo responsavel por excluir aula do modulo do curso, so é possivel
excluir se o modulo não possuir aulas cadastradas
"""

@login_required
@is_creator
def deletar_aula_moduloView(request,slug,pk):

    aula = get_object_or_404(aulas_curso,id = pk)

    aula.delete()
    messages.info(request,'Aula excluida com sucesso!!')
    

    #redireciona para pagina que solicitou a operação
    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))


@login_required
@is_creator
def cadastrar_material_curso(request,slug):

    template_name = 'form.html'
    form = material_cursoform(request.POST,request.FILES or None)
    
    if form.is_valid():
        
        form.instance.curso = request.curso
        form.save()
        
        messages.info(request,'Material com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-criados')))
    
    context = {'form': form,'titulo':'Cadastrar Material do Curso','botao':'Cadastrar'}

    return render(request,template_name,context)

#View responsavel por editar um material do curso
class Edit_materialView(GroupRequiredMixin,UpdateView):
    
    group_required = u'professor'
    template_name = 'form.html'
    model = materiais_curso
    fields = ['titulo','material']

    def get_object(self, queryset = None):

       curso = get_object_or_404(modelcursos,slug = self.kwargs['slug'],user = self.request.user)
       object = get_object_or_404(materiais_curso,id = self.kwargs['pk'])

       return object

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Editar Material do curso'
        context['botao'] = 'Salvar Alterações'

        return context
    
    #redireciona a pagina anterior que solicitou a edição
    def get_success_url(self):
        
        messages.info(self.request,'Alterações salvas com sucesso!!')

        return self.request.GET.get('next', reverse_lazy('meus-cursos-criados'))

@login_required
@is_creator
def deletar_material_cursoView(request,slug,pk):

    material = get_object_or_404(materiais_curso,id = pk)

    material.delete()
    messages.info(request,'Material excluido com sucesso!!')
    

    #redireciona para pagina que solicitou a operação
    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))



class Ver_materiais_curso(ListView):
    template_name = 'cursos/materiais_curso.html'
    model = materiais_curso

    def get_queryset(self, queryset = None):
        curso = get_object_or_404(modelcursos, slug = self.kwargs['slug'])

        return curso.materiais.all()


@login_required
@matriculado
def aulaView(request,slug,pk):
    template_name = 'cursos/aula.html'

    aula = get_object_or_404(aulas_curso, id=pk)
    curso = get_object_or_404(modelcursos, slug=slug)

    context = {'aula': aula, 'curso': curso}

    return render(request,template_name,context)

@login_required
@is_creator
def Enviar_aviso(request,slug):

    template_name = 'form.html'
    form = avisos_cursoform(request.POST or None)
    
    if form.is_valid():
        
        form.instance.curso = request.curso
        form.save()
        
        messages.info(request,'Aviso enviado com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-criados')))
    
    context = {'form': form,'titulo':'Enviar Aviso','botao':'Enviar'}

    return render(request,template_name,context)


class Ver_avisos_curso(ListView):
    template_name = 'cursos/avisos_curso.html'
    model = avisos_curso

    def get_queryset(self, queryset = None):
        curso = get_object_or_404(modelcursos, slug = self.kwargs['slug'])

        return curso.avisos.all()
    
@login_required
def conteudo_view(request):
    
    template_name = "cursos/dashboard/conteudo.html"
    cursos = request.user.modelcursos_set.all()

    context = {'cursos': cursos, 'curso_selecionado': False}

    return render(request, template_name, context)


@login_required
def detalhesView_dash(request, slug):

    template_name = "cursos/dashboard/detalhes.html"
    curso = get_object_or_404(modelcursos, slug=slug)

    context = {'curso': curso, 'curso_selecionado': False}

    return render(request, template_name, context)


@login_required
def visualizarAulas_dash(request, slug):

    template_name = "cursos/dashboard/aulas_curso.html"
    curso = get_object_or_404(modelcursos, slug=slug)

    context = {'curso': curso, 'curso_selecionado': False}

    return render(request, template_name, context)


class CadastroCurso_dash(GroupRequiredMixin, CreateView):

    group_required = u'professor'
    model = modelcursos
    """
    utilizando o CreateView não é nescessario criar um formulario para o model
    pois ele ja cria o formulario automaticamente com base nas fields definidas
    form = cadastrocurso
    
    """
    fields = ['nome', 'descricao', 'sobre_curso',
              'data_inicio', 'image', 'categoria']

    template_name = 'cursos/dashboard/form.html'

    success_url = reverse_lazy('cursos')

    """
    for_valid serve para rescrever função de validação do CreateView, para isso basta
    passar o form do createview, para acessar atributos do form usa: form.instance.atributo
    e para salvar form utiliza o metodo return super().form_valid(form)
    
    """

    def get_form(self, form_class=None):
        form = super(CadastroCurso_dash, self).get_form(form_class)
        form.fields['data_inicio'].widget = DateInput()
        return form

    def form_valid(self, form):

        slug_curso = slug(form.instance.nome) + '-' + \
            self.request.user.username + '-' + f'{random.randint(0,1000)}'

        form.instance.slug = slug_curso
        form.instance.user = self.request.user

        form.save()

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Criar Curso'
        context['botao'] = 'Criar'
        context['need_'] = True

        return context
    

@login_required
def aulaView_dash(request, slug, pk):
    template_name = 'cursos/dashboard/aula_view.html'

    aula = get_object_or_404(aulas_curso, id=pk)
    curso = get_object_or_404(modelcursos, slug=slug)

    context = {'aula': aula, 'curso': curso}
    
    return render(request, template_name, context)
