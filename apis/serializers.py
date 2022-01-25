from rest_framework import serializers
from posts.models import User, Post, Comment, PostsVotes


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "link", "author", "created_at", "votes"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "content", "author", "created_at"]
