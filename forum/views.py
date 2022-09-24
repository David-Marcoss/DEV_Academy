from multiprocessing import context
from re import template
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from accounts.models import User
from cursos.decorator import is_creator,matriculado

from django.core.paginator import Paginator

from .models import *
from .forms import *
from django.db.models import Q


@login_required
@matriculado
def forumView(request,slug):

    template_name = 'cursos/forum/forum.html'
    
    curso = request.curso
    forum = Forum.objects.get(curso=curso)
    topicos = forum.get_topicos()

    busca = request.GET.get("Busca")
    
    if busca:
        topicos = topicos.filter( Q(titulo__icontains = busca ) | Q(autor__nome__icontains = busca ) 
        | Q(assunto__icontains = busca ))

    ordering = request.GET.get('ordering')


    """
    atraves do parametro ordering passado pela URL
    determino como vai ser listado os topicos
    """
    if  ordering == 'recentes':
        topicos = topicos.order_by('-criado_em')
    
    elif ordering == 'populares':
        topicos = topicos.order_by('-num_respostas')
    
    elif ordering == 'nao respondidos':
        topicos = topicos.filter(num_respostas=0)
    
    elif ordering == 'meus topicos':
        topicos = topicos.filter(autor=request.user)
    
    elif ordering == 'antigos':
        topicos = topicos.order_by('criado_em')


    #define a quantidade de itens por pagina
    paginator = Paginator(topicos,10)
    #pega atravez da url o numero da pagina atual
    page_number = request.GET.get('page')
    #pega os objetos da pagina passada
    page_obj = paginator.get_page(page_number)
    
    return render(request,template_name,context = {'curso':curso,'forum':forum,'page_obj':page_obj,'paginator':paginator})


@login_required
@matriculado
def detalhes_topicoView(request,slug,pk):

    template_name = 'cursos/forum/detalhes-topico.html'
    context = {}

    topico = Topicos.objects.get(id = pk)
    respostas = topico.get_respostas()
    ordering = request.GET.get('ordering')

    if request.user != topico.autor:
        topico.visualizacoes += 1
        topico.save() 

    if  ordering == 'recentes':
        respostas = respostas.order_by('-criado_em')
    
    elif ordering == 'antigas':
        respostas = respostas.order_by('criado_em')

    elif ordering == 'mais curtidas':
        respostas = respostas.order_by('-like')
        
    
    context['topico'] = topico
    context['respostas'] = respostas
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

        topico.num_respostas= topico.respostas.all().count() 
        topico.save() 

        #messages.info(request,'Topico Criado com Sucesso!!')
        
        return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))
    
    context = {'form': form,'titulo': 'Responder Topico do Curso', 'botao': 'Responder'}

    return render(request,template_name,context)
        

@login_required
@matriculado
def like_respostaView(request,slug,pk):
    resposta = get_object_or_404(Respostas,id=pk)

    if like.objects.filter(resposta = resposta,user=request.user).exists():
        Like = like.objects.get(resposta = resposta,user=request.user)
        Like.delete()

        resposta.like -= 1
        resposta.save()
    else:
       Like = like(resposta = resposta,user=request.user)
       Like.save()

       resposta.like += 1
       resposta.save()

    return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))

@login_required
def deletar_topicoView(request,pk,slug):
    topico = get_object_or_404(Topicos,id=pk,autor=request.user)
    forum = topico.forum
    topico.delete()

    return redirect('forum-curso',slug=slug)
