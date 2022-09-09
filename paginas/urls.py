from django.urls import path
from .views import contatoview, homeview, dashview


urlpatterns = [
    path('contato/',contatoview.as_view(),name='contato'),
    path('home/', homeview.as_view(), name='home'),
    path('dashview/', dashview.as_view(), name='dashview'),

]

