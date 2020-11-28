from rest_framework import serializers
from blog.models import Category,Post
from django.contrib.auth.models import User



class PostSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','author','excerpt','content','status')


class UserSerializer(serializers.ModelSerializer):
    """ User """
    class Meta:
        model = User
        fields = ('id','username','email') 


class RegisterSerializer(serializers.ModelSerializer):
    """Register"""
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validate_data):
        user = User.objects.create_user(validate_data['username'],validate_data['email'],validate_data['password'])

        return user