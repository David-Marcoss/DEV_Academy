import hashlib
import string
import random

"""
    funções auxiliares uzadas para redefinição de senha do usuario
"""

"""
estas funções servem para gerar uma string com valores aleatorios
para que sirva como uma chave para gerar um link unico para que
o usuario consiga alterar sua senha 

"""
def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

def generate_hash_key(salt, random_str_size=5):
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()

"""função recebe o tempo e acresenta 1h ao tempo recebido"""

def acesentar_tempo(time):
    time = str(time)
    time = time.split(':')

    time = f'{ int(time[0]) + 1}'+ ':'+ time[1] + ':' + time[2]

    return time



"""
   recebe o tempo1 que representa o tempo o tempo que o usuario esta acessando a pagina
   e o tempo2 que é o tempo em que a pagina pode ser acessado e verifica os tempos se o
   tempo 1 for maior que o tempo 2 quer dizer que o tempo expirou 

"""
def compara_tempo(tempo1,tempo2):

    tempo1 = str(tempo1).split(':')
    tempo2 = str(tempo2).split(':')

    expirou = None

    i = 0
    while(i < len(tempo1) and expirou == None):

        tempo1[i] = float(tempo1[i])
        tempo2[i] = float(tempo2[i])

        if tempo2[i] > tempo1[i]:
            expirou = False

        elif tempo2[i] < tempo1[i]:
            expirou = True

        i += 1

    if expirou == None:
        expirou = True

    return expirou
