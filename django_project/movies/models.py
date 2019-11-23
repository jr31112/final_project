from django.db import models

# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)


class People(models.Model):
    id = models.IntegerField(primary_key=True)
    ko_name = models.CharField(max_length=30)
    en_name = models.CharField(max_length=30)
    birthday = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10)
    is_alive = models.BooleanField()
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