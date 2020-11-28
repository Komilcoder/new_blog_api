from django.contrib import admin
from .models import Category,Post


@admin.register(Category)
class AuthorCategory(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Post)
class AuthorPost(admin.ModelAdmin):
    list_display = ('title','id','status','slug','content')
    prepopulated_fields = {'slug':('title',),}
