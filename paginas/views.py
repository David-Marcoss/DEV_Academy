from django.views.generic import TemplateView

# Create your views here.

class contatoview(TemplateView):
    template_name = "contact.html"


class homeview(TemplateView):
    template_name = "home.html"
