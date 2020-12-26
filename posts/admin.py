from django.contrib import admin

# Register your models here.

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):

    #pk - primary key
    list_display = ("pk", "text", "pub_date", "author")

    search_fields = ("text", )

    list_filter = ("pub_date", "author")

    empty_value_display = "-пусто-"


admin.site.register(Post, PostAdmin)

admin.site.register(Group)
