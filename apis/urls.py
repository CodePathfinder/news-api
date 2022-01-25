from django.urls import path
from . import views

urlpatterns = [
    path("newslist", views.NewsList.as_view()),
    path("myposts", views.MyPosts.as_view()),
    path("postdetails/<int:pk>", views.PostDetails.as_view()),
]
