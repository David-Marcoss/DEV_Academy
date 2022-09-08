from .models import aulas_curso,modelcursos


def quantidade_aulas(modulo):
    aulas  = aulas_curso.objects.filter(id = modulo)
    list_aulas= []
    
    for i in aulas:
        list_aulas.append(i)

    return aulas

def retorna_aulas_curso(slug):

    curso = modelcursos.objects.get(slug=slug)

    modulos = curso.modulo.all()
    
    aulas_curso = {}

    for i in modulos:
        aulas_curso[i] = quantidade_aulas(i.id)
    
    return aulas_curso


"""
recebe um link do video do youtube e faz tratamento 
para que o video possa ser incorporado no site

"""
def trata_link(video):

    link = 'https://www.youtube.com/embed/'
    video = video.split('/')

    id_video = video[-1]

    id_video = id_video.replace('watch?v=','')
  
    link += id_video

    return link


import validators

"""
recebe um link e verifica se o link é valido
"""
def verifica_link(video):
    
    valid=validators.url(video)

    link = link = 'https://www.youtube.com/'
    link2 = 'https://youtu.be/'

    if valid and video != link:

        if link != video[:len(link)] and link2 != video[:len(link2)] :
            valid = False

    else:
        valid = False
    
    return valid

    

