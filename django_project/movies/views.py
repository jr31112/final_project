from django.shortcuts import render, get_object_or_404
from .serializers import MovieUpdateSerializers, PersonDetailSerializers, UserReviewSerializers, ReviewSerializers, ReviewUserSerializers
from .models import Movie, Genre, People, Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
# Create your views here.
@api_view(['GET'])
def movie_index(request):
    movies = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieUpdateSerializers(movies, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieUpdateSerializers(movie)
    return Response(serializer.data)
        

@api_view(['GET'])
def person_detail(request, person_pk):
    person = get_object_or_404(People, pk=person_pk)
    serializer = PersonDetailSerializers(person)
    return Response(serializer.data)

@api_view(['GET'])
def finder(request, query):
    movies = Movie.objects.filter(title__contains=query)
    peoples = People.objects.filter(ko_name__contains=query)
    serializer_movies = MovieUpdateSerializers(movies, many=True)
    serializer_peoples = PersonDetailSerializers(peoples, many=True)
    return Response(serializer_movies.data + serializer_peoples.data)

@api_view(['GET'])
def user_detail(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    serializer = UserReviewSerializers(user)
    return Response(serializer.data)

@api_view(['GET'])
def reviews(request):
    review = Review.objects.all().order_by('-id')[:10]
    serializer = ReviewSerializers(review, many=True)
    return Response(serializer.data) 

@api_view(['POST'])
def review_create(request, movie_pk, user_pk):
    print(request.data)
    serializer = ReviewUserSerializers(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk, user_id=user_pk)
    return Response({'message' : '리뷰가 작성되었습니다.'})

@api_view(['PUT', 'DELETE'])
def update_delete_review(request, review_pk, user_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user.pk != user_pk:
            return Response({'message' : '사용자가 일치하지 않습니다.'})
    if request.method == 'PUT':
        serializer = ReviewUserSerializers(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '성공적으로 수정 되었습니다.'})
    else:
        review.delete()
        return Response({'message': '성공적으로 삭제 되었습니다.'})

    
