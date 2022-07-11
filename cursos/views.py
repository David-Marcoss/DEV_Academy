from pyexpat import model
from urllib import request
from django.views.generic import TemplateView,ListView
from .models import cursos

from django.shortcuts import render, get_object_or_404
                     

# Create your views here.

class cursosview(ListView):

    model = cursos
    template_name = 'cursos.html'


def detalhes_cursoview(request,slug):
    
    course = get_object_or_404(cursos, slug=slug) #função busca um elemento de uma tabela
    
    context = {'course': course} #contexto serve para passar um objeto para um template

    template_name = 'detalhes_curso.html'
    
    return render(request, template_name, context)

