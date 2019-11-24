from django.shortcuts import render, get_object_or_404
from .serializers import MovieUpdateSerializers, PersonDetailSerializers
from .models import Movie, Genre, People
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def movie_index(request):
    movies = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieUpdateSerializers(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieUpdateSerializers(movie)
    return Response(serializer.data)

@api_view(['GET'])
def person_detail(request, person_pk):
    person = get_object_or_404(People, pk=person_pk)
    serializer = PersonDetailSerializers(person)
    return Response(serializer.data)