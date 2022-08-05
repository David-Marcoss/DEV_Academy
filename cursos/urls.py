from django.urls import path
from .views import cursosview,detalhes_cursoview,CadastroCursoview


urlpatterns = [
    path('cursos/',cursosview.as_view(),name='cursos'),
    path('cursos/detalhes/<str:slug>/',detalhes_cursoview,name='detalhes-curso'),
    path('cursos/cadastrar/',CadastroCursoview.as_view(),name='cadastrar-curso'),

]