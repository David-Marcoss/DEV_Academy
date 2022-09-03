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
    

