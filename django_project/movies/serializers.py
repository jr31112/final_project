from rest_framework import serializers
from .models import Movie, Genre, People, Review
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer, SimpleUserSerializer

class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class PeopleSerializers(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['id', 'ko_name', 'en_name', 'birthday', 'gender','deathday', 'popularity', 'place_of_birth', 'img_url']

class MovieSerializers(serializers.ModelSerializer): 
    class Meta:
        model = Movie
        fields = ['id', 'title', 'overview', 'release_date', 'img_url', 'country', 'rating', 'popularity', 'trailer', 'runtime']

class SimpleReviewSerializers(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    class Meta:
        model = Review
        fields = ['id', 'content', 'user_score'] + ['user']

class MovieUpdateSerializers(serializers.ModelSerializer):
    actors = PeopleSerializers(many=True)
    genres = GenreSerializers(many=True)
    director = PeopleSerializers()
    review_set = SimpleReviewSerializers(many=True)
    class Meta:
        model =  Movie
        fields = MovieSerializers.Meta.fields + ['genres'] + ['director'] + ['actors'] + ['review_set']

class PersonDetailSerializers(serializers.ModelSerializer):
    actor_movies = MovieSerializers(many=True)
    movie_set = MovieSerializers(many=True)
    class Meta:
        model = People
        fields = PeopleSerializers.Meta.fields + ['actor_movies'] +['movie_set']

class ReviewSerializers(serializers.ModelSerializer):
    movie = MovieSerializers()
    class Meta:
        model = Review
        fields = ['id', 'content', 'user_score'] + ['movie']

class UserReviewSerializers(serializers.ModelSerializer):
    review_set = ReviewSerializers(many=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'username'] + ['review_set']


class ReviewUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'content', 'user_score']