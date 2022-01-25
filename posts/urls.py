from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_comment/<int:post_id>", views.add_comment, name="add_comment"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("update_votes/<int:post_id>", views.update_votes, name="update_votes"),
]
