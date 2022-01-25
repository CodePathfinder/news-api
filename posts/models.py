from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class Post(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author"
    )
    title = models.CharField(max_length=128)
    link = models.CharField(max_length=2048)
    # path = models.FileField(upload_to='media/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, through="PostsVotes", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def comments_count(self):
        return Comment.objects.filter(post__id=self.id).count()

    def votes_count(self):
        return (
            PostsVotes.objects.filter(post=self.id, is_voted=True)
            .exclude(user=self.author)
            .count()
        )

    def __str__(self):
        return f"post {self.id} of {self.author.username}"


class PostsVotes(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts_posts_votes"
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="voted"),
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_author"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"New comment for {self.post} by {self.author.username}"

    class Meta:
        ordering = ["-created_at"]
