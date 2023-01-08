from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit.post import post_service
from flaskeddit.reply import reply_blueprint, reply_service
from flaskeddit.reply.forms import ReplyForm


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply", methods=["GET", "POST"]
)
@login_required
def reply(name, title):
    """
    Route for creating a reply. On a GET request, it returns the reply creation form.
    On a POST request, it handles creating a reply.
    """
    post = post_service.get_post(title, name)
    if post:
        form = ReplyForm()
        if form.validate_on_submit():
            reply_service.create_reply(form.reply.data, post, current_user)
            flash("Successfully created reply.", "primary")
            return redirect(url_for("post.post", name=name, title=title))
        return render_template("create_reply.html", name=name, title=title, form=form)
    else:
        abort(404)


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def update_reply(name, title, reply_id):
    """
    Route for updating a reply. On a GET request, it returns the reply update form. On
    a POST request, it handles updating a reply.
    """
    reply = reply_service.get_reply(reply_id)
    if reply:
        if reply.user_id != current_user.id:
            return redirect(url_for("post.post", name=name, title=title))
        form = ReplyForm()
        if form.validate_on_submit():
            reply_service.update_reply(reply, form.reply.data)
            flash("Successfully updated reply.", "primary")
            return redirect(url_for("post.post", name=name, title=title))
        form.reply.data = reply.reply
        return render_template(
            "update_reply.html", name=name, title=title, reply_id=reply_id, form=form
        )
    else:
        abort(404)


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/delete",
    methods=["POST"],
)
@login_required
def delete_reply(name, title, reply_id):
    """
    Route that handles deleting a reply.
    """
    reply = reply_service.get_reply(reply_id)
    if reply:
        if reply.user_id != current_user.id:
            return redirect(url_for("post.post", name=name, title=title))
        reply_service.delete_reply(reply)
        flash("Successfully deleted reply.", "primary")
        return redirect(url_for("post.post", name=name, title=title))
    else:
        abort(404)


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/upvote",
    methods=["POST"],
)
@login_required
def upvote_reply(name, title, reply_id):
    """
    Route that handles upvoting a reply as the current user.
    """
    reply = reply_service.get_reply(reply_id)
    if reply:
        reply_service.upvote_reply(reply_id, current_user.id)
        return redirect(request.referrer)
    else:
        abort(404)


@reply_blueprint.route(
    "/community/<string:name>/post/<string:title>/reply/<int:reply_id>/downvote",
    methods=["POST"],
)
@login_required
def downvote_reply(name, title, reply_id):
    """
    Route that handles downvoting a reply as the current user.
    """
    reply = reply_service.get_reply(reply_id)
    if reply:
        reply_service.downvote_reply(reply_id, current_user.id)
        return redirect(request.referrer)
    else:
        abort(404)
