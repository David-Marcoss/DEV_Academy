from django.urls import path

from forum.views import forumView

urlpatterns = [
    path('<str:slug>/',forumView,name='forum-curso'),

]