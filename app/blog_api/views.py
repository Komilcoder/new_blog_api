from django.shortcuts import render
from blog.models import Category,Post
from .serializers import PostSeriaizer,UserSerializer,RegisterSerializer
from rest_framework.views import APIView
from rest_framework import status,generics,permissions
from django.http import Http404
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class PostListView(APIView):
    """ all List and CreateViews """

    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        post = Post.objects.all()
        serializer = PostSeriaizer(post,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = PostSeriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class PostDetailView(APIView):
    """ Retrieve , Update and DeleteViews """

    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        post = self.get_object(pk)
        serializer = PostSeriaizer(post)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        post = self.get_object(pk)
        serializer = PostSeriaizer(post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class RegisterView(generics.GenericAPIView):
    """ Registration """

    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def post(self,request, *args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user":UserSerializer(user,context=self.get_serializer_context()).data,"token":AuthToken.objects.create(user)[1]})



class LoginApi(KnoxLoginView):
    """ Login """

    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user) 
        return super(LoginApi,self).post(request,format=None)       



