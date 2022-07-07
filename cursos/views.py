from pyexpat import model
from django.views.generic import TemplateView,ListView
from .models import cursos

# Create your views here.

class cursosview(ListView):

    model = cursos
    template_name = 'cursos.html'


class detalhes_cursoview(TemplateView):

    model = cursos
    template_name = 'detalhes_curso.html'

