from django.views.generic import TemplateView
from cursos.models import categoria_curso, modelcursos
from accounts.models import User
from braces.views import GroupRequiredMixin

from django.shortcuts import get_list_or_404,render, get_object_or_404,redirect
from django.urls import reverse_lazy
from cursos.models import modelcursos
from django.db.models import Q

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
        allProf = User.objects.all().filter(is_Teacher=True).values()
        context['Prof_01'] = allProf[:1][0] if allProf[:1] else None
        context['Prof_02'] = allProf[1:2][0] if allProf[1:2] else None
        context['Prof_03'] = allProf[2:3][0] if allProf[2:3] else None
        
        # Categorias
        allCategorias = categoria_curso.objects.all()
        context['firstCategorias'] = allCategorias.values()[0:1][0] if allCategorias.values()[0:1] else None
        context['secondCategorias'] = allCategorias.values()[1:2][0] if allCategorias.values()[1:2] else None
        context['thirdCategorias'] = allCategorias.values()[2:3][0] if allCategorias.values()[2:3] else None
        context['fourthCategorias'] = allCategorias.values()[3:4][0] if allCategorias.values()[3:4] else None
        context['fifthCategorias'] = allCategorias.values()[4:5][0] if allCategorias.values()[4:5] else None
        context['sixthCategorias'] = allCategorias.values()[5:6][0] if allCategorias.values()[5:6] else None
        
        # Cursos por categoria
        context['categoria01'] = modelcursos.objects.all().filter(
            categoria=allCategorias[0:1][0].id).values() if allCategorias.values()[0:1] else None
        context['categoria02'] = modelcursos.objects.all().filter(
            categoria=allCategorias[1:2][0].id).values() if allCategorias.values()[1:2] else None
        context['categoria03'] = modelcursos.objects.all().filter(
            categoria=allCategorias[2:3][0].id).values() if allCategorias.values()[2:3] else None
        context['categoria04'] = modelcursos.objects.all().filter(
            categoria=allCategorias[3:4][0].id).values() if allCategorias.values()[3:4] else None
        context['categoria05'] = modelcursos.objects.all().filter(
            categoria=allCategorias[4:5][0].id).values() if allCategorias.values()[4:5] else None
        context['categoria06'] = modelcursos.objects.all().filter(
            categoria=allCategorias[5:6][0].id).values() if allCategorias.values()[5:6] else None
        
        # context['categoria01'] = modelcursos.objects.all().filter(categoria=allCategorias[0:1][0].id).values()
        # context['categoria02'] = modelcursos.objects.all().filter(categoria=allCategorias[1:2][0].id).values()
        # context['categoria03'] = modelcursos.objects.all().filter(categoria=allCategorias[2:3][0].id).values()
        # context['categoria04'] = modelcursos.objects.all().filter(categoria=allCategorias[3:4][0].id).values()
        # context['categoria05'] = modelcursos.objects.all().filter(categoria=allCategorias[4:5][0].id).values()
        # context['categoria06'] = modelcursos.objects.all().filter(categoria=allCategorias[5:6][0].id).values()

        return context

class dashview(GroupRequiredMixin, TemplateView):
    group_required = u'professor'
    template_name = "paginas/home_dash.html"


def searchView(request):

    template_name = 'cursos/cursos.html'

    busca = request.GET.get("Busca")

    object_list = modelcursos.objects.filter(
        Q(nome__icontains = busca ) | Q(user__nome__icontains = busca ) 
        | Q(categoria__categoria__icontains = busca )  

    )

    return render(request,template_name,context={'object_list':object_list,'titulo':f"Resutados para a busca: {busca}"})

