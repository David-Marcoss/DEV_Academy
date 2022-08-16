from django.views.generic import TemplateView
from cursos.models import modelcursos

# Create your views here.

class contatoview(TemplateView):
    template_name = "paginas/contact.html"


class homeview(TemplateView):
    template_name = "paginas/home.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        todos_cursos = modelcursos.objects.all()      
        context['top_cursos'] = todos_cursos[:6]
        return context
