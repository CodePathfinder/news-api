
from .models import PostsVotes


def reset_upvotes():

    post_votes = PostsVotes.objects.filter(is_voted=True)

    for p_vote in post_votes:
        p_vote.is_voted = False
        p_vote.save()
