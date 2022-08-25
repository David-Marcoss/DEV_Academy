from django.urls import path
from .views import cursosview,detalhes_cursoview,CadastroCursoview,Edit_cursoview,matriculaview


urlpatterns = [
    path('cursos/',cursosview.as_view(),name='cursos'),
    path('cursos/detalhes/<str:slug>/',detalhes_cursoview,name='detalhes-curso'),
    path('cursos/cadastrar/',CadastroCursoview.as_view(),name='cadastrar-curso'),
    path('cursos/edit-curso/<int:pk>/',Edit_cursoview.as_view(),name='edit-curso'),
    path('cursos/matricular-se/<str:slug>/',matriculaview,name='matricula'),
]