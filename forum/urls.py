from django.urls import path

from forum.views import *

urlpatterns = [
    path('<str:slug>/',forumView,name='forum-curso'),
    path('<str:slug>/topico/<int:pk>/',detalhes_topicoView,name='detalhes-topico'),
    path('<str:slug>/criar-topico/<int:pk>/',criar_topicoView,name='criar-topico'),
    path('<str:slug>/responder-topico/<int:pk>/',responder_topicoView,name='responder-topico'),
    path('<str:slug>/like-resposta/<int:pk>/',like_respostaView,name='like-resposta'),

]