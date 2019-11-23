from django.urls import path, include
from . import views
urlpatterns = [
    path('movies/', views.movie_index, name='movie_index'),
    path('genres/', views.genre_index, name='genre_index'),
    path('people/', views.people_index, name='people_index'),
]