from flaskeddit import db
from flaskeddit.models import AppUser, Community, CommunityMember, Post, PostVote


def get_community(name):
    """
    Gets a community by name from the database.
    """
    community = Community.query.filter_by(name=name).first()
    return community


def create_community(name, description, user):
    """
    Adds a new community to the database.
    """
    community = Community(name=name, description=description, app_user=user)
    db.session.add(community)
    db.session.commit()


def update_community(community, description):
    """
    Updates an existing community's description in the database.
    """
    community.description = description
    db.session.commit()


def delete_community(community):
    """
    Removes a community from the database.
    """
    db.session.delete(community)
    db.session.commit()


def get_community_posts(community_id, page, ordered_by_votes):
    """
    Gets paginated list of posts from a specified community from the database.
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
        )
        .outerjoin(PostVote, Post.id == PostVote.post_id)
        .join(AppUser, Post.user_id == AppUser.id)
        .filter(Post.community_id == community_id)
        .group_by(Post.id, AppUser.id)
        .order_by(ordered_by)
        .paginate(page=page, per_page=5)
    )
    return posts


def get_community_member(community_id, user_id):
    """
    Gets a community membership by community and user from the database.
    """
    community_member = CommunityMember.query.filter_by(
        community_id=community_id, user_id=user_id
    ).first()
    return community_member


def create_community_member(community, user):
    """
    Adds a new community member to the database.
    """
    community_member = CommunityMember(community=community, app_user=user)
    db.session.add(community_member)
    db.session.commit()


def delete_community_member(community_member):
    """
    Removes a community member from the database.
    """
    db.session.delete(community_member)
    db.session.commit()
