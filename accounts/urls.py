from re import template
from django.urls import path,include
from django.conf import settings
from django.contrib.auth import views as auth_views

from .views import cadastroview,perfilview,UserUpdate,UserpasswordUpdate,redefinir_senhaview,reset_passwordview

urlpatterns = [
   path('login/',auth_views.LoginView.as_view(template_name = 'login.html'),name='login'),
   path('logout/',auth_views.LogoutView.as_view(),name='logout'),
   path('cadastrar/',cadastroview,name='cadastrar'),
   path('perfil/',perfilview,name='perfil'),
   path('edit-perfil/<int:pk>/',UserUpdate.as_view(),name='edit-perfil'),
   path('edit-password/',UserpasswordUpdate,name='edit-password'),
   path('redefinir-senha/',redefinir_senhaview,name='redefinir-senha'),
   path('reset-password/<str:key>/',reset_passwordview,name='reset-password'),
   
   
   
]

# auth_views.LoginView.as_view() ésta função serve para implementar a view padrao do django para 
#login
