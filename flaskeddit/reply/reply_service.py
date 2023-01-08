from flaskeddit import db
from flaskeddit.models import Post, Reply, ReplyVote


def get_reply(reply_id):
    """
    Gets a reply by ID from the database.
    """
    reply = Reply.query.get(reply_id)
    return reply


def create_reply(reply, post, user):
    """
    Adds a new reply to the database.
    """
    reply = Reply(reply=reply, post=post, app_user=user)
    db.session.add(reply)
    db.session.commit()


def update_reply(reply, reply_text):
    """
    Updates a reply's text content in the database.
    """
    reply.reply = reply_text
    db.session.commit()


def delete_reply(reply):
    """
    Removes a reply from the database.
    """
    db.session.delete(reply)
    db.session.commit()


def get_reply_vote(reply_id, user_id):
    """
    Gets a specific user's vote on a reply the database.
    """
    reply_vote = ReplyVote.query.filter_by(user_id=user_id, reply_id=reply_id).first()
    return reply_vote


def upvote_reply(reply_id, user_id):
    """
    Upvotes a reply for a user in the database. If the reply is already voted on, undo
    the vote.
    """
    reply_vote = get_reply_vote(reply_id, user_id)
    if reply_vote is None:
        reply_vote = ReplyVote(vote=1, user_id=user_id, reply_id=reply_id)
        db.session.add(reply_vote)
    elif abs(reply_vote.vote) == 1:
        reply_vote.vote = 0
    else:
        reply_vote.vote = 1
    db.session.commit()


def downvote_reply(reply_id, user_id):
    """
    Downvotes a reply for a user in the database. If the reply is already voted on,
    undo the vote.
    """
    reply_vote = get_reply_vote(reply_id, user_id)
    if reply_vote is None:
        reply_vote = ReplyVote(vote=-1, user_id=user_id, reply_id=reply_id)
        db.session.add(reply_vote)
    elif abs(reply_vote.vote) == 1:
        reply_vote.vote = 0
    else:
        reply_vote.vote = -1
    db.session.commit()
