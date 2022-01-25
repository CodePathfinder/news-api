from django.contrib import admin
from .models import User, Post, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
    list_display_links = ("id", "username")
    search_fields = ("username",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "link", "author", "created_at")
    list_display_links = ("id", "title", "link")
    order_by = "id"
    search_fields = ("title", "author")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "content", "author", "created_at")
    list_display_links = ("id", "post", "author")
    order_by = "author"
    search_fields = ("post", "author")


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
