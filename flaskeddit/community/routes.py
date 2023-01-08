from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from flaskeddit.user import user_service
from flaskeddit.community import community_blueprint, community_service
from flaskeddit.community.forms import CommunityForm, UpdateCommunityForm


@community_blueprint.route("/community/<string:name>")
def community(name):
    """
    Route for page displaying a community and its posts sorted by date created.
    """
    page = int(request.args.get("page", 1))
    community = community_service.get_community(name)
    if community:
        posts = community_service.get_community_posts(community.id, page, False)
        community_member = None
        if current_user.is_authenticated:
            community_member = community_service.get_community_member(
                community.id, current_user.id
            )
            user, email, moderator = user_service.get_user(current_user.username)
            return render_template(
                "community.html",
                tab="recent",
                community=community,
                posts=posts,
                community_member=community_member,
                app_user=user,
                )
        else:
            return render_template(
                "community.html",
                tab="recent",
                community=community,
                posts=posts,
                community_member=community_member,
                )
    else:
        abort(404)


@community_blueprint.route("/community/<string:name>/top")
def top_community(name):
    """
    Route for page displaying a community and its posts sorted by number of upvotes.
    """
    page = int(request.args.get("page", 1))
    community = community_service.get_community(name)
    if community:
        posts = community_service.get_community_posts(community.id, page, True)
        community_member = None
        if current_user.is_authenticated:
            community_member = community_service.get_community_member(
                community.id, current_user.id
            )
            isModerator = user_service.get_user(current_user.username).moderator
        return render_template(
            "community.html",
            tab="top",
            community=community,
            posts=posts,
            community_member=community_member,
            isModerator = isModerator,
        )
    else:
        abort(404)


@community_blueprint.route("/community/create", methods=["GET", "POST"])
@login_required
def create_community():
    """
    Route for creating a community. On a GET request, it returns the community creation
    form. On a POST request, it processes a community creation.
    """
    form = CommunityForm()
    if form.validate_on_submit():
        community_service.create_community(
            form.name.data, form.description.data, current_user
        )
        flash("Successfully created community.", "primary")
        return redirect(url_for("community.community", name=form.name.data))
    return render_template("create_community.html", form=form)


@community_blueprint.route("/community/<string:name>/update", methods=["GET", "POST"])
@login_required
def update_community(name):
    """
    Route for updating a community description. On a GET request, it returns the update
    community form. On a POST request, it processes the community update.
    """
    community = community_service.get_community(name)
    if community:
        if community.user_id != current_user.id:
            return redirect(url_for("community.community", name=name))
        form = UpdateCommunityForm()
        if form.validate_on_submit():
            community_service.update_community(community, form.description.data)
            flash("Successfully updated community.", "primary")
            return redirect(url_for("community.community", name=name))
        form.description.data = community.description
        return render_template("update_community.html", name=name, form=form)
    else:
        abort(404)


@community_blueprint.route("/community/<string:name>/delete", methods=["POST"])
@login_required
def delete_community(name):
    """
    Route that handles deleting a community.
    """
    community = community_service.get_community(name)
    if community:
        if community.user_id != current_user.id:
            return redirect(url_for("community.community", name=name))
        community_service.delete_community(community)
        flash("Successfully deleted community.", "primary")
        return redirect(url_for("feed.feed"))
    else:
        abort(404)


@community_blueprint.route("/community/<string:name>/join", methods=["POST"])
@login_required
def join_community(name):
    """
    Route that handles adding the current user as a community member.
    """
    community = community_service.get_community(name)
    if community:
        community_member = community_service.get_community_member(
            community.id, current_user.id
        )
        if community_member == None:
            community_service.create_community_member(community, current_user)
        flash("Successfully joined community.", "primary")
        return redirect(url_for("community.community", name=community.name))
    else:
        abort(404)


@community_blueprint.route("/community/<string:name>/leave", methods=["POST"])
@login_required
def leave_community(name):
    """
    Route that handles removing the current user as a community member.
    """
    community = community_service.get_community(name)
    if community:
        community_member = community_service.get_community_member(
            community.id, current_user.id
        )
        if community_member:
            community_service.delete_community_member(community_member)
        flash("Successfully left community.", "primary")
        return redirect(url_for("community.community", name=community.name))
    else:
        abort(404)
