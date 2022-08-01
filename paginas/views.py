from django.views.generic import TemplateView

# Create your views here.

class contatoview(TemplateView):
    template_name = "paginas/contact.html"


class homeview(TemplateView):
    template_name = "paginas/home.html"
