from email.mime import image
from pyexpat import model
from urllib import request
from django.views.generic import TemplateView,ListView,CreateView
from .models import modelcursos
from .forms import contatocurso,cadastrocurso

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from slug import slug
                     

# Create your views here.

class cursosview(ListView):

    model = modelcursos
    template_name = 'cursos/cursos.html'


def detalhes_cursoview(request,slug):
    context = {}
    course = get_object_or_404(modelcursos, slug=slug) #função busca um elemento de uma tabela
    
    if request.method == 'POST':  #verifica se foi enviado um foemulario com o metodo Post
       form = contatocurso(request.POST) #request.POST retorna um discionario com os atributos enviados do formulario

       if form.is_valid():
           context['is_valid'] = True
           
           #print(form.cleaned_data['nome']) para acessar os campos do formulario deve se utilizar a funçao form.cleaned_data['campo']
           
           form.enviar_email(course)
           form = contatocurso()

    else:
        form = contatocurso()

    context['course'] =  course #contexto serve para passar um objeto para um template
    context['form'] =  form 

    template_name = 'cursos/detalhes_curso.html'
    
    return render(request, template_name, context)

class CadastroCursoview(CreateView):
    
    model = modelcursos
    form = cadastrocurso
    fields = ['nome','descricao','sobre_curso','data_inicio','image']
    
    template_name = 'form.html'

    
    success_url= reverse_lazy('cursos')

    def form_valid(self, form):

        form.cleaned_data['slug'] = slug(form.cleaned_data['nome'])

        form.save()

        return super().form_valid(form)

    def get_context_data(self, *args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        context['titulo'] = 'Criar Curso'
        context['botao'] = 'Criar'

        return context
        

