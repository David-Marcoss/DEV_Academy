from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from accounts.models import User

from .models import modelcursos,matricula


"""
decorador que permite que apenas o usuario que criou o
curso tenha acesso a determinada view
"""
def is_creator(view_func):
    
    def _wrapper(request,*args,**kargs):
        slug = kargs['slug']
        curso = get_object_or_404(modelcursos,slug = slug,user = request.user)
        request.curso = curso
        
        return view_func(request,*args,**kargs)
    
    return _wrapper

"""
decorador que permite que apenas o usuario que criou o
curso e os alunos matriculados no curso tenha acesso 
a determinada view
"""
def matriculado(view_func):
    
    def _wrapper(request,*args,**kargs):
        slug = kargs['slug']
        
        curso = get_object_or_404(modelcursos,slug = slug)
        
        if not matricula.objects.filter(curso=curso,user=request.user).exists() and not curso.user == request.user:
            messages.info(request,'Para acessar aulas e materiais do curso voce precia se increver no curso!!')
            return redirect(request.GET.get('next', reverse_lazy('meus-cursos-matriculados')))

        return view_func(request,*args,**kargs)
    
    return _wrapper