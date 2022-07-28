from re import template
from django.urls import path,include
from django.conf import settings
from django.contrib.auth import views as auth_views

from .views import cadastroview

urlpatterns = [
   path('login/',auth_views.LoginView.as_view(template_name = 'login.html'),name='login'),
   path('logout/',auth_views.LogoutView.as_view(),name='logout'),
   path('cadastrar/',cadastroview,name='cadastrar'),
   
]

# auth_views.LoginView.as_view() ésta função serve para implementar a view padrao do django para 
#login
