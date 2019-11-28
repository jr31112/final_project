from django.contrib import admin
from .models import Movie, Genre, People, Review
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(People)
admin.site.register(Review)