from django.urls import path
from .views import cursosview,detalhes_cursoview


urlpatterns = [
    path('cursos/',cursosview.as_view(),name='cursos'),
    path('cursos/detalhes/<str:slug>/',detalhes_cursoview,name='detalhes-curso'),

]