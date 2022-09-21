from multiprocessing import context
from re import template
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import UpdateView,ListView,CreateView,DeleteView

from accounts.models import User
from cursos.decorator import is_creator,matriculado

from .models import *
from .forms import *


@login_required
@matriculado
def forumView(request,slug):

    template_name = 'cursos/forum/forum.html'
    context = {}
    curso = request.curso
    
    context['curso'] = curso
    context['forum'] = Forum.objects.get(curso=curso)

    return render(request,template_name,context)


@login_required
@matriculado
def detalhes_topicoView(request,slug,pk):

    template_name = 'cursos/forum/detalhes-topico.html'
    context = {}

    topico = Topicos.objects.get(id = pk)

    if request.user != topico.autor:
        topico.visualizacoes += 1
        topico.save() 
        
    
    context['topico'] = topico
    context['curso'] = request.curso

    return render(request,template_name,context)


@login_required
@matriculado
def criar_topicoView(request,slug,pk):
    template_name = 'form.html'
    form = Topicoform(request.POST or None)

    if form.is_valid():
        form.instance.forum = get_object_or_404(Forum,id=pk)
        form.instance.autor = request.user
        form.save()

        #messages.info(request,'Topico Criado com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))
    
    context = {'form': form,'titulo': 'Criar Topico do Curso', 'botao': 'Criar'}

    return render(request,template_name,context)


@login_required
@matriculado
def responder_topicoView(request,slug,pk):
    template_name = 'form.html'
    form = Respostaform(request.POST or None)

    if form.is_valid():
        topico = get_object_or_404(Topicos,id=pk)
        form.instance.topico = topico
        form.instance.autor = request.user
        form.save()

        topico.num_respostas += 1
        topico.save() 

        #messages.info(request,'Topico Criado com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))
    
    context = {'form': form,'titulo': 'Responder Topico do Curso', 'botao': 'Responder'}

    return render(request,template_name,context)
        

@login_required
@matriculado
def like_respostaView(request,slug,pk):
    resposta = get_object_or_404(Respostas,id=pk)
    resposta.like += 1
    resposta.save()

    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))