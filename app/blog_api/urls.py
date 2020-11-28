from django.urls import path
from . import views
from knox import views as knox_views


urlpatterns = [
    path('',views.PostListView.as_view(),name='post-list'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post-detail'),
    path('register',views.RegisterView.as_view(),name='post-register'),
    path('login',views.LoginApi.as_view(),name='login'),
    path('logout',knox_views.LogoutView.as_view(),name='logout'),
    path('logoutall',knox_views.LogoutAllView.as_view(),name='logoutall'),


]
