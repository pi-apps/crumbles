from flaskeddit import db
from flaskeddit.models import AppUser, Community, CommunityMember, Post, PostVote


def get_feed(user, page, ordered_by_votes):
    """
    Get paginated list of posts from communities that a given user is a member of from
    the database.
    """
    ordered_by = Post.date_created.desc()
    if ordered_by_votes:
        ordered_by = db.literal_column("votes").desc()
    posts = (
        db.session.query(
            Post.title,
            Post.post,
            Post.date_created,
            db.func.coalesce(db.func.sum(PostVote.vote), 0).label("votes"),
            AppUser.username,
            Community.name.label("community_name"),
        )
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .join(AppUser, Post.user_id == AppUser.id)
        .join(Community, Post.community_id == Community.id)
        .join(CommunityMember, Post.community_id == CommunityMember.community_id)
        .filter(CommunityMember.user_id == user.id)
        .group_by(Post.id, AppUser.id, Community.id)
        .order_by(ordered_by)
        .paginate(page=page, per_page=5)
    )
    return posts
