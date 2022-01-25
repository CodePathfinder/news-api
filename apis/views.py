from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from posts.models import Post
from .serializers import PostSerializer, CommentSerializer


def post_dict(post):

    """Helper function"""

    author_name = post.author.username
    author = post.author.id
    serializer = PostSerializer(post)
    post_dict = serializer.data
    post_dict["author_name"] = author_name
    post_dict["author"] = author
    votes = len(post_dict["votes"])
    post_dict["votes"] = votes
    return post_dict


class NewsList(APIView):

    """Retrieve all posts"""

    def get(self, request):
        posts = Post.objects.all()
        posts_list = []
        for post in posts:
            p_dict = post_dict(post)
            posts_list.append(p_dict)
        print(posts_list)
        return Response(posts_list, status=status.HTTP_200_OK)


class MyPosts(APIView):

    """Retrieve current user's posts"""

    def get(self, request):
        posts = Post.objects.filter(author=request.user.id)
        posts_list = []
        for post in posts:
            p_dict = post_dict(post)
            posts_list.append(p_dict)
        print(posts_list)
        return Response(posts_list, status=status.HTTP_200_OK)

    """Add post by current user"""

    def post(self, request):

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid() and request.user.id == request.data["author"]:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetails(APIView):
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    """Retreve any post and all comments thereto"""

    def get(self, request, pk):
        post = self.get_post(pk)
        p_dict = post_dict(post)
        print(p_dict)

        comments = post.comments.all()
        print()
        comments_list = []
        for comment in comments:
            author = comment.author.username
            serializer = CommentSerializer(comment)
            comment_dict = serializer.data
            comment_dict["author"] = author
            comment_dict.pop("post")
            comments_list.append(comment_dict)

        print(request.user)
        return Response({"Post": p_dict, "Comments": comments_list})

    def put(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post, data=request.data)
        if request.user != post.author:
            return Response(
                {"Error": "Update forbidden"}, status=status.HTTP_403_FORBIDDEN
            )
        if request.user.id != request.data["author"]:
            return Response(
                {"Error": "Bad request, check author id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid() and request.user == post.author:
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        post = self.get_post(pk)
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"Error": "Deletion forbidden"}, status=status.HTTP_403_FORBIDDEN
        )
