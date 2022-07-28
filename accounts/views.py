from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import is_valid_path
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings

from DMS_cursos.settings import LOGIN_REDIRECT_URL


def cadastroview(request):

    template_name = "cadastro.html"

    if request.method == 'POST': # verifica se o meto de formulario é post
        
        form = UserCreationForm(request.POST) #requeste armazena os dados preencidos pelo ususario

        if form.is_valid(): #verifica se o formulario é valido
            form.save() # salva os dados do form no banco

            return redirect(LOGIN_REDIRECT_URL)
    
    
    else:
        form = UserCreationForm()


    context = { 'form':  form }

    return render(request,template_name,context)

