from rest_framework import serializers
from .models import Movie, Genre, People
from accounts.serializers import UserSerializer

class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class PeopleSerializers(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['id', 'ko_name', 'en_name', 'birthday', 'gender', 'is_alive', 'popularity', 'place_of_birth', 'img_url']

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'overview', 'release_date', 'img_url', 'country', 'rating', 'popularity']

class MovieUpdateSerializers(serializers.ModelSerializer):
    actors = PeopleSerializers(many=True)
    genres = GenreSerializers(many=True)
    director = PeopleSerializers()
    class Meta:
        model =  Movie
        fields = MovieSerializers.Meta.fields + ['genres'] + ['director'] + ['actors']

class PersonDetailSerializers(serializers.ModelSerializer):
    actor_movies = MovieSerializers(many=True)
    movie_set = MovieSerializers(many=True)
    class Meta:
        model = People
        fields = PeopleSerializers.Meta.fields + ['actor_movies'] +['movie_set']


