from django.shortcuts import render
from .serializers import MovieSerializers, GenreSerializers, PeopleSerializers, MovieUpdateSerializers
from .models import Movie, Genre, People
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def movie_index(request):
    movies = Movie.objects.all()
    serializer = MovieSerializers(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_index(request):
    genres = Genre.objects.all()
    serialize = GenreSerializers(genres, many=True)
    return Response(serialize.data)

@api_view(['GET'])
def people_index(request):
    people = People.objects.all()
    serializer = PeopleSerializers(people, many=True)
    return Response(serializer.data)

