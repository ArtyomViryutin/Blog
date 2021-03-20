from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Comment, Follow, Group, Post

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'group', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    # empty_value_display = '-пусто-'
    readonly_fields = ('get_image',)
    form = PostAdminForm
    fieldsets = (
        (None, {
            'fields': (('author',),)
        }),
        (None, {
            'fields': (('group',),)
        }),
        (None, {
            'fields': (('text',),)
        }),
        (None, {
            'fields': (('image',), 'get_image')
        })
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150"')
    get_image.short_description = 'Изображение'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class CommentAmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'text')


admin.site.register(Group, GroupAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Comment, CommentAmin)

admin.site.site_title = 'Блог'
admin.site.site_header = 'Блог'

