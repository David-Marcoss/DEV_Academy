from .models import modulo_curso

""" 
insere numero da aula no model aula, essa
operação é realizada quando é inserida uma
nova aula, ou quando é excluida uma aula

"""
def atualiza_numero_aulas(curso):
    num_aula = 0

    for modulos in curso.get_modulos():
        for aulas in modulos.get_aulas():
            num_aula += 1 
            aulas.numero_aula = num_aula
            aulas.save()

""" 
insere numero do modulo no model aula, essa
operação é realizada quando é inserida um
novo modulo, ou quando é excluida um modulo

"""
def atualiza_numero_modulo(curso):
    num_modulo = 0

    for modulo in curso.get_modulos():
        num_modulo += 1 
        modulo.numero_modulo = num_modulo
        modulo.save()


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

    

