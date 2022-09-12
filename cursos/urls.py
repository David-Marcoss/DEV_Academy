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
    path('cursos/excluir-modulo/<str:slug>/<int:pk>/',deletar_modulo_cursoView,name='excluir-modulo-curso'),
    path('cursos/criar-aula-modulo/<str:slug>/<int:pk>/',cadastrar_aula_modulo_cursoView,name='criar-aula-modulo'),
    path('cursos/modulos-curso/aulas/<str:slug>/<int:pk>/',ver_aulas_modulos_cursoView.as_view(),name='aulas-modulo-curso'),
    path('cursos/modulos-curso/editar-aula/<str:slug>/<int:pk>/',Edit_aula_moduloView.as_view(),name='edit-aula-modulo-curso'),
    path('cursos/modulos-curso/excluir-aula/<str:slug>/<int:pk>/',deletar_aula_moduloView,name='deletar-aula-modulo-curso'),
    path('cursos/modulos-curso/aula/<int:pk>/',aulaView,name='ver-aula'),
    path('cursos/cadastrar-material/<str:slug>/',cadastrar_material_curso,name='cadastrar-material'),
    path('cursos/editar-material/<str:slug>/<int:pk>/',Edit_materialView.as_view(),name='editar-material'),
    path('cursos/excluir-material/<str:slug>/<int:pk>/',deletar_material_cursoView,name='deletar-material'),
    path('cursos/materiais/<str:slug>/',Ver_materiais_curso.as_view(),name='materiais-curso'),
    path('cursos/enviar-aviso/<str:slug>/',Enviar_aviso,name='enviar-aviso'),
    path('cursos/avisos/<str:slug>/',Ver_avisos_curso.as_view(),name='avisos-curso'),
    path('conteudo_view', conteudo_view, name='conteudo_view'),
    path('detalhesView_dash/<str:slug>/', detalhesView_dash, name='detalhesView_dash'),
]
