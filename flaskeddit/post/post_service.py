from flaskeddit import db
from flaskeddit.models import AppUser, Community, Post, PostVote, Reply, ReplyVote


def get_post(title, community_name):
    """
    Gets a post from a specified community by title from the database.
    """
    post = (
        db.session.query(Post)
        .join(Community, Post.community_id == Community.id)
        .filter(Post.title == title)
        .filter(Community.name == community_name)
        .first()
    )
    return post


def get_post_with_votes(title, community_name):
    """
    Gets a post with vote information from a specified community by title from the
    database.
    """
    post = (
        db.session.query(
            Post.id,
            Post.title,
            Post.post,
            Post.date_created,
            Post.user_id,
            db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
            AppUser.username,
            Community.name.label("community_name"),
            Community.description.label("community_description"),
        )
        .join(AppUser, Post.user_id == AppUser.id)
        .join(Community, Post.community_id == Community.id)
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .filter(Post.title == title)
        .filter(Community.name == community_name)
        .group_by(Post.id, AppUser.id, Community.id)
        .first()
    )
    return post


def create_post(title, post, community, user):
    """
    Adds a new post for the specified community to the database.
    """
    post = Post(title=title, post=post, community=community, app_user=user)
    db.session.add(post)
    db.session.commit()


def update_post(post, post_text):
    """
    Updates a post's text content in the database.
    """
    post.post = post_text
    db.session.commit()


def delete_post(post):
    """
    Removes a post from the database.
    """
    db.session.delete(post)
    db.session.commit()


def get_post_replies(post_id, page, ordered_by_votes):
    """
    Gets paginated list of replies for a specified post from the database.
    """
    ordered_by = Reply.date_created.desc()
    if ordered_by_votes:
        ordered_by = db.literal_column("votes").desc()
    replies = (
        db.session.query(
            Reply.id,
            Reply.reply,
            Reply.user_id,
            Reply.date_created,
            db.func.coalesce(db.func.sum(ReplyVote.vote), 0).label("votes"),
            AppUser.username,
        )
        .join(AppUser, Reply.user_id == AppUser.id)
        .outerjoin(ReplyVote, Reply.id == ReplyVote.reply_id)
        .filter(Reply.post_id == post_id)
        .group_by(Reply.id, AppUser.id)
        .order_by(ordered_by)
        .paginate(page=page, per_page=5)
    )
    return replies


def get_post_vote(post_id, user_id):
    """
    Gets a specific user's vote on a post the database.
    """
    post_vote = PostVote.query.filter_by(user_id=user_id, post_id=post_id).first()
    return post_vote


def upvote_post(post_id, user_id):
    """
    Upvotes a post for a user in the database. If the post is already voted on, undo the
    vote.
    """
    post_vote = get_post_vote(post_id, user_id)
    if post_vote is None:
        post_vote = PostVote(vote=1, user_id=user_id, post_id=post_id)
        db.session.add(post_vote)
    elif abs(post_vote.vote) == 1:
        post_vote.vote = 0
    else:
        post_vote.vote = 1
    db.session.commit()


def downvote_post(post_id, user_id):
    """
    Downvotes a post for a user in the database. If the post is already voted on, undo the
    vote.
    """
    post_vote = get_post_vote(post_id, user_id)
    if post_vote is None:
        post_vote = PostVote(vote=-1, user_id=user_id, post_id=post_id)
        db.session.add(post_vote)
    elif abs(post_vote.vote) == 1:
        post_vote.vote = 0
    else:
        post_vote.vote = -1
    db.session.commit()
