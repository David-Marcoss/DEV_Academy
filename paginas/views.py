from django.views.generic import TemplateView
from cursos.models import categoria_curso, modelcursos
from accounts.models import User
from braces.views import GroupRequiredMixin
from django.db.models import Count

from django.shortcuts import get_list_or_404

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
        
        # Professores
        allProf = User.objects.filter(is_Teacher=True).values()
        context['Prof_01'] = allProf[:1][0] if allProf[:1] else None
        context['Prof_02'] = allProf[1:2][0] if allProf[1:2] else None
        context['Prof_03'] = allProf[2:3][0] if allProf[2:3] else None
        
        # Categorias
        """
            Preferir mandar variaveis que contem as seis primeiras categorias do que pegar de cada curso
            a categoria que eles pertecem.
        """
        allCategorias = categoria_curso.objects.all()
        context['firstCategorias'] = allCategorias.values()[0:1][0] if allCategorias.values()[0:1] else None
        context['secondCategorias'] = allCategorias.values()[1:2][0] if allCategorias.values()[1:2] else None
        context['thirdCategorias'] = allCategorias.values()[2:3][0] if allCategorias.values()[2:3] else None
        context['fourthCategorias'] = allCategorias.values()[3:4][0] if allCategorias.values()[3:4] else None
        context['fifthCategorias'] = allCategorias.values()[4:5][0] if allCategorias.values()[4:5] else None
        context['sixthCategorias'] = allCategorias.values()[5:6][0] if allCategorias.values()[5:6] else None
        
        # Cursos por categoria
        context['categoria01'] = modelcursos.objects.filter(categoria=1)[:8]
        context['categoria02'] = modelcursos.objects.filter(categoria=2)[:8]
        context['categoria03'] = modelcursos.objects.filter(categoria=3)[:8]
        context['categoria04'] = modelcursos.objects.filter(categoria=4)[:8]
        context['categoria05'] = modelcursos.objects.filter(categoria=5)[:8]
        context['categoria06'] = modelcursos.objects.filter(categoria=6)[:8]
        
        # Cursos mais assistidos
        context['maisAssistidos'] = modelcursos.objects.annotate(num_matricula=Count('matricula')).order_by('-num_matricula')
        
        # Categorias da plataforma
        context['prin_categorias'] = categoria_curso.objects.all()[:8]

        return context

class dashview(GroupRequiredMixin, TemplateView):
    group_required = u'professor'
    template_name = "paginas/home_dash.html"
