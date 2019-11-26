from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator 
# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class People(models.Model):
    id = models.IntegerField(primary_key=True)
    ko_name = models.CharField(max_length=30)
    en_name = models.CharField(max_length=30)
    birthday = models.CharField(max_length=30, null=True)
    deathday = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10)
    popularity = models.FloatField()
    place_of_birth = models.TextField(null=True)
    img_url = models.TextField(null=True)



class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre, related_name='movies')
    overview = models.TextField(null=True)
    release_date = models.CharField(max_length=30)
    actors = models.ManyToManyField(People, related_name='actor_movies')
    director = models.ForeignKey(People, on_delete=models.PROTECT)
    img_url = models.TextField(null=True)
    country = models.CharField(max_length=50)
    rating = models.FloatField()
    popularity = models.FloatField()
    runtime = models.IntegerField(null=True)
    trailer = models.TextField(null=True)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    user_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
