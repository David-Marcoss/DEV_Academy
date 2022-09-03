from django.urls import path
from .views import *


urlpatterns = [
    path('cursos/',cursosview.as_view(),name='cursos'),
    path('cursos/detalhes/<str:slug>/',detalhes_cursoview,name='detalhes-curso'),
    path('cursos/cadastrar/',CadastroCursoview.as_view(),name='cadastrar-curso'),
    path('cursos/edit-curso/<int:pk>/',Edit_cursoview.as_view(),name='edit-curso'),
    path('cursos/matricular-se/<str:slug>/',matriculaview,name='matricula'),
    path('cursos/meus-cursos-matriculados/',Meus_cursos_matriculados_view.as_view(),name='meus-cursos-matriculados'),
    path('cursos/meus-cursos-criados/',Meus_cursos_criados_view.as_view(),name='meus-cursos-criados'),
    path('cursos/cancelar-matricula/<int:pk>/',Cancelar_matriculaview,name='cancelar-matricula'),
    path('cursos/modulos-curso/<str:slug>/',ver_modulos_cursoView.as_view(),name='modulos-curso'),
    path('cursos/criar-modulo/<str:slug>/',cadastrar_modulo_cursoView,name='criar-modulo-curso'),
    path('cursos/editar-modulo/<str:slug>/<int:pk>/',Edit_moduloView.as_view(),name='editar-modulo-curso'),
    path('cursos/criar-aula-modulo/<str:slug>/<int:pk>/',cadastrar_aula_modulo_cursoView,name='criar-aula-modulo'),
    path('cursos/modulos-curso/aulas/<str:slug>/<int:pk>/',ver_aulas_modulos_cursoView.as_view(),name='aulas-modulo-curso'),

]
