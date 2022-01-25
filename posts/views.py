from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import User, Post, Comment, PostsVotes
from .forms import NewComment


def index(request):

    posts = Post.objects.all()

    context = {
        "posts": posts,
    }
    return render(request, "posts/index.html", context)


def add_comment(request, post_id):

    post = Post.objects.get(id=post_id)
    comments = post.comments.all()

    if request.method == "POST":

        if not request.user.is_authenticated:
            messages.warning(request, "Please login to add comments")
            return redirect("login")

        form = NewComment(request.POST)

        if form.is_valid():
            comment = Comment(
                post=post,
                content=form.cleaned_data["content"],
                author=request.user,
            )
            # Save new bid object and update two fields (current_price and updated_at) AuctionListings table re commodity at issue
            comment.save()
            messages.success(
                request,
                f'Your comment "{comment.content}" is succesfully added to post "{post.title}"',
            )
            return redirect("index")
        else:
            messages.error(request, "Validation error")
            context = {
                "post": post,
                "comments": comments,
                "form": form,
            }
            return render(request, "posts/add_comment.html", context)
    else:
        context = {
            "post": post,
            "comments": comments,
            "form": NewComment(),
        }
        return render(request, "posts/add_comment.html", context)


@api_view(["GET", "POST"])
def update_votes(request, post_id):

    post = Post.objects.get(id=post_id)
    # current user cannot add votes to his/her own post
    if post.author == request.user:
        pass
    elif post.votes.filter(id=request.user.id).exists():
        check_vote_status = PostsVotes.objects.get(post=post, user=request.user.id)
        check_vote_status.is_voted = not check_vote_status.is_voted
        check_vote_status.save()
    else:
        post.votes.add(request.user)
    return Response({"votes_count": post.votes_count()}, status=status.HTTP_200_OK)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "posts/login.html")
    else:
        return render(request, "posts/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]

        if not username or not password:
            messages.error(
                request, "Invalid request. Please enter username and password."
            )
            return render(request, "posts/register.html")

        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords does not match.")
            return render(request, "posts/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "posts/register.html")
        login(request, user)
        return redirect("index")
    else:
        return render(request, "posts/register.html")
