from multiprocessing import context
from re import template
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.views.generic import UpdateView,ListView,CreateView,DeleteView

from accounts.models import User
from cursos.decorator import is_creator,matriculado

from .models import *


@login_required
@matriculado
def forumView(request,slug):

    template_name = 'cursos/forum/forum.html'
    context = {}
    curso = request.curso
    
    context['curso'] = curso
    context['forum'] = Forum.objects.get(curso=curso)

    return render(request,template_name,context)