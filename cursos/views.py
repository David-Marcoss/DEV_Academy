from pyexpat import model
from urllib import request
from django.views.generic import TemplateView,ListView
from .models import cursos
from .forms import contatocurso

from django.shortcuts import render, get_object_or_404
                     

# Create your views here.

class cursosview(ListView):

    model = cursos
    template_name = 'cursos/cursos.html'


def detalhes_cursoview(request,slug):
    context = {}
    course = get_object_or_404(cursos, slug=slug) #função busca um elemento de uma tabela
    
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

