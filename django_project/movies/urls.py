from django.urls import path, include
from . import views
urlpatterns = [
    path('movies/', views.movie_index, name='movie_index'),
    path('movies/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('people/<int:person_pk>/', views.person_detail, name='person_detail'),
    path('search/<str:query>/', views.finder, name='finder'),
    path('user/<int:user_pk>/', views.user_detail, name='user_detail'),
    path('reviews/', views.reviews, name='reviews'),
]