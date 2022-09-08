from django.views.generic import TemplateView
from cursos.models import modelcursos
from accounts.models import User

# Create your views here.

class contatoview(TemplateView):
    template_name = "paginas/contact.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = 'Fale conosco'

        return context

class homeview(TemplateView):
    template_name = "paginas/home.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        allProf = User.objects.all().filter(is_Teacher=True).values()
        context['Prof_01'] = allProf[:1][0] if allProf[:1] else None
        context['Prof_02'] = allProf[1:2][0] if allProf[1:2] else None
        context['Prof_03'] = allProf[2:3][0] if allProf[2:3] else None
        return context
