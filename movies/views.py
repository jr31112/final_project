from django.shortcuts import render, get_object_or_404
from .serializers import MovieUpdateSerializers, PersonDetailSerializers, UserReviewSerializers, ReviewSerializers, ReviewUserSerializers
from .models import Movie, Genre, People, Review
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.db.models.query import EmptyQuerySet
# Create your views here.
@api_view(['GET'])
def movie_index(request):
    if request.GET.get('user_id'):
        user_id = request.GET.get('user_id')
        tmp_reviews = Review.objects.all()
        critics = {}
        movies = Movie.objects.none()
        for j in range(len(tmp_reviews)):
            tmp_review = tmp_reviews[j]
            # print(tmp_review) 
            if critics.get(tmp_review.user.pk):
                critics[tmp_review.user.pk].update({tmp_review.movie.pk:tmp_review.user_score})
            else:
                critics.update({tmp_review.user.pk:{tmp_review.movie.pk:tmp_review.user_score}})
        movie_list = getRecommendation(critics, user_id)
        for _, idx in movie_list:
            movies.union(Movie.objects.get(pk=idx))
        if isinstance(movies, EmptyQuerySet):
            movies = Movie.objects.all().order_by('-popularity')[:10]
    else:
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

# collaborative filtering
from math import sqrt

# 피어슨 상관계수 구하기
def sim_pearson(data, name1, name2):
    name1, name2 = int(name1), int(name2)
    sumX=0 # X의 합
    sumY=0 # Y의 합
    sumPowX=0 # X 제곱의 합
    sumPowY=0 # Y 제곱의 합
    sumXY=0 # X*Y의 합
    count=0 #영화 개수
    for i in data[name1]: # i = key
        if i in data[name2]: # 같은 영화를 평가했을때만
            sumX+=data[name1][i]
            sumY+=data[name2][i]
            sumPowX+=pow(data[name1][i],2)
            sumPowY+=pow(data[name2][i],2)
            sumXY+=data[name1][i]*data[name2][i]
            count+=1
    return ( sumXY- ((sumX*sumY)/count) )/ sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count))) if sqrt( (sumPowX - (pow(sumX,2) / count)) * (sumPowY - (pow(sumY,2)/count))) else -1

# 딕셔너리 돌면서 상관계수순으로 정렬
def top_match(data, name, index=10, sim_function=sim_pearson):
    li=[]
    name = int(name)
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort(reverse=True) #정렬
    return li[:index]

def getRecommendation (data,person,sim_function=sim_pearson):
    result = top_match(data, person ,len(data))
    
    simSum=0 # 유사도 합을 위한 변수
    score=0 # 평점 합을 위한 변수
    li=[] # 리턴을 위한 리스트
    score_dic={} # 유사도 총합을 위한 dic
    sim_dic={} # 평점 총합을 위한 dic
 
    for sim,name in result:
        if sim<0 : continue #유사도가 양수인 사람만
        for movie in data[name]: 
            if movie not in data[person]: #name이 평가를 내리지 않은 영화
                score+=sim*data[name][movie] # 그사람의 영화평점 * 유사도
                score_dic.setdefault(movie,0) # 기본값 설정
                score_dic[movie]+=score # 합계 구함
 
                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(movie,0) 
                sim_dic[movie]+=sim
 
            score=0  #영화가 바뀌었으니 초기화한다
    
    for key in score_dic: 
        score_dic[key]=score_dic[key]/sim_dic[key] # 평점 총합/ 유사도 총합
        li.append((score_dic[key],key)) # list((tuple))의 리턴을 위해서.
    li.sort(reverse=True) # 정렬
    return li