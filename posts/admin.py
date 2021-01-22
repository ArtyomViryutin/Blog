from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text', )
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class CommentAmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'text')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAmin)