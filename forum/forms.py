from django import forms

from .models import Topicos,Respostas

class Topicoform(forms.ModelForm):
     
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
          self.fields['assunto'].widget.attrs.update({'class': 'form-control'})
          self.fields['notificacoes'].widget.attrs.update({'class': 'form-check-input'})
        
     class Meta:
          model = Topicos
          fields = ['titulo','assunto','notificacoes']    


class Respostaform(forms.ModelForm):
     class Meta:
          model = Respostas
          fields = ['resposta']