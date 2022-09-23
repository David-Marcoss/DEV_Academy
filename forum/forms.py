from django import forms

from .models import Topicos,Respostas

class Topicoform(forms.ModelForm):
     class Meta:
          model = Topicos
          fields = ['titulo','assunto','notificacoes']


class Respostaform(forms.ModelForm):
     class Meta:
          model = Respostas
          fields = ['resposta']