import datetime

from flask_login import UserMixin

from flaskeddit import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    Loader used to reload the user object from the user ID stored in the session.
    https://flask-login.readthedocs.io/en/latest/#how-it-works
    """
    return AppUser.query.get(user_id)


class AppUser(db.Model, UserMixin):
    """Model that represents a user."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    moderator = db.Column(db.Boolean, default=False, nullable=False)
    pi_username = db.Column(db.String(255), unique=True)
    pi_wallet = db.Column(db.String(56), unique=True)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    communities = db.relationship(
        "Community", backref="app_user", lazy="dynamic", cascade="all, delete-orphan"
    )
    posts = db.relationship(
        "Post", backref="app_user", lazy="dynamic", cascade="all, delete-orphan"
    )
    replies = db.relationship(
        "Reply", backref="app_user", lazy="dynamic", cascade="all, delete-orphan"
    )
    post_votes = db.relationship(
        "PostVote", backref="app_user", lazy="dynamic", cascade="all, delete-orphan"
    )
    reply_votes = db.relationship(
        "ReplyVote", backref="app_user", lazy="dynamic", cascade="all, delete-orphan"
    )
    community_members = db.relationship(
        "CommunityMember",
        backref="app_user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<AppUser (id='{self.id}', username='{self.username}')>"


class Community(db.Model):
    """Model that represents a community."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), unique=True, nullable=False)
    description = db.Column(db.UnicodeText, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    posts = db.relationship(
        "Post", backref="community", lazy="dynamic", cascade="all, delete-orphan"
    )
    community_members = db.relationship(
        "CommunityMember",
        backref="community",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Community (id='{self.id}', name='{self.name}', description='{self.description}', date_created='{self.date_created}')>"


class Post(db.Model):
    """Model that represents a post."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    post = db.Column(db.UnicodeText, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)
    replies = db.relationship(
        "Reply", backref="post", lazy="dynamic", cascade="all, delete-orphan"
    )
    post_votes = db.relationship(
        "PostVote", backref="post", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post (id='{self.id}', title='{self.title}', post='{self.post}', date_created='{self.date_created}')>"


class Reply(db.Model):
    """Model that represents a reply."""

    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Unicode, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    reply_votes = db.relationship(
        "ReplyVote", backref="reply", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Reply (id='{self.id}', reply='{self.reply}', date_created='{self.date_created}')>"


class PostVote(db.Model):
    """Model that tracks a user's vote on a post."""

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __repr__(self):
        return f"<PostVote (id='{self.id}', vote='{self.vote}')>"


class ReplyVote(db.Model):
    """Model that tracks a user's vote on a reply."""

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    reply_id = db.Column(db.Integer, db.ForeignKey("reply.id"), nullable=False)

    def __repr__(self):
        return f"<ReplyVote (id='{self.id}', vote='{self.vote}')>"


class CommunityMember(db.Model):
    """Model that tracks a user's community membership."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.id"), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("community.id"), nullable=False)

    def __repr__(self):
        return f"<CommunityMember (id='{self.id}')>"
