from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Review

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    like_movies = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True)
    class Meta:
        model = get_user_model()
        fields =['id', 'username', 'password', 'password2' , 'like_movies']
    
    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        non_alpha = set([s for s in "!@#$%^&*()|-=_+\[]{};':\",./?><"])
        error = dict({'username' : [], 'password': []})
        if data['password'] != data['password2']: # confirm error: 1
            error['password'].append('비밀번호 같게 해주세요')
        if not 8 <= len(data['password']) < 16:   # password length error: 2
            error['password'].append('비밀번호를 8 ~ 16자로 작성해주세요!')
        if data['password'].isdigit():  # password is only numbers: 3
            error['password'].append('비밀번호를 다른 문자와 조합해주세요!')
        if get_user_model().objects.filter(username= data['username']): # same username in db : 4
            error['username'].append('중복된 ID가 있습니다.')
        if not 0 < len(data['username']) < 16:  # username length error: 5 
            error['username'].append('ID를 1 ~ 16 글자로 해주세요!')
        for word in data['username']: # non_alph in username: 6
            if word in non_alpha:
                error['username'].append('ID에 특수문자를 넣지 말아주세요!')
                break

        return error

class UserIndexSerializer(serializers.ModelSerializer):
    review_set = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), many=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'username'] + ['review_set']

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']

