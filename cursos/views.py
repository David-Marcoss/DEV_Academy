from email.mime import image
from multiprocessing import context
from pyexpat import model
from re import template
from tokenize import group
from urllib import request
from django.views.generic import UpdateView,ListView,CreateView
from .models import modelcursos,matricula
from .forms import contatocurso

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from slug import slug
import random
from django.contrib.auth.decorators import login_required

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


def detalhes_cursoview(request,slug):
    context = {}
    
    course = get_object_or_404(modelcursos, slug=slug) #função busca um elemento de uma tabela
    
    criador = get_object_or_404(User, username = course.user)
    
    
    form = contatocurso(request.POST or None) #request.POST retorna um discionario com os atributos enviados do formulario

    if form.is_valid():
        context['is_valid'] = True
        
        form.enviar_email(course,criador.email)
        form = contatocurso()


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
    fields = ['nome','descricao','sobre_curso','data_inicio','image']
    
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

@login_required
def matriculaview(request,slug):
    
    template_name = 'cursos/detalhes_curso.html'
    
    criador = get_object_or_404(User, username = curso.user)
    curso = get_object_or_404(modelcursos, slug=slug)

    if matricula.objects.filter(user = request.user,curso = curso).exists():
        success = False
    else:
        model.curso = curso
        model.user = request.user
        model = model.save()
        success = True
    
    context = {'sucess': success }

    return render(request,template_name,context)
    