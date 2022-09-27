from django.contrib import admin

from .models import * 

class TopicosAdmin(admin.ModelAdmin):

    list_display = ['titulo', 'autor', 'criado_em', 'atualizado_em']
    search_fields = ['titulo', 'author__email', 'assunto']


class RespostasAdmin(admin.ModelAdmin):

    list_display = ['resposta','topico','autor', 'criado_em', 'atualizado_em']
    search_fields = ['Topicos__title', 'author__email', 'resposta']


admin.site.register(Forum)
admin.site.register(Topicos,TopicosAdmin)
admin.site.register(Respostas,RespostasAdmin)