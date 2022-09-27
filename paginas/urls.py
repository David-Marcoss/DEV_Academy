from django.urls import path
from .views import contatoview, homeview, dashview,searchView


urlpatterns = [
    path('', homeview.as_view(), name='home'),
    path('home/', homeview.as_view(), name='home'),
    path('contato/',contatoview.as_view(),name='contato'),
    path('dashview/', dashview.as_view(), name='dashview'),
    path('search/', searchView, name='search'),
]

