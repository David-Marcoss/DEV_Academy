from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import modelcursos

def is_creator(view_func):
    
    def _wrapper(request,*args,**kargs):
        slug = kargs['slug']
        curso = get_object_or_404(modelcursos,slug = slug,user = request.user)
        request.curso = curso
        
        return view_func(request,*args,**kargs)
    
    return _wrapper