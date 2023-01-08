from flaskeddit import db
from flaskeddit.models import AppUser, Community, CommunityMember


def get_communities(page):
    """
    Gets paginated list of communities by date created from the database.
    """
    communities = (
        db.session.query(
            Community.id,
            Community.name,
            Community.description,
            Community.date_created,
            Community.user_id,
            AppUser.username,
        )
        .join(AppUser, Community.user_id == AppUser.id)
        .order_by(Community.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return communities


def get_communities_by_membership(page):
    """
    Gets paginated list of communities by number of members from the database.
    """
    communities = (
        db.session.query(
            Community.id,
            Community.name,
            Community.description,
            Community.date_created,
            Community.user_id,
            AppUser.username,
            db.func.count(CommunityMember.id).label("community_members"),
        )
        .join(AppUser, Community.user_id == AppUser.id)
        .outerjoin(CommunityMember, Community.id == CommunityMember.community_id)
        .group_by(Community.id, AppUser.id)
        .order_by(db.literal_column("community_members").desc())
        .paginate(page=page, per_page=5)
    )
    return communities
