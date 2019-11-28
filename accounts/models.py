from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie 
# Create your models here.

class User(AbstractUser):
    like_movies = models.ManyToManyField(Movie, related_name="like_users", blank=True)
    
    
