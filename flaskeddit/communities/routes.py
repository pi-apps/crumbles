from flask import render_template, request

from flaskeddit.communities import communities_blueprint, communities_service


@communities_blueprint.route("/communities")
def communities():
    """
    Route for page displaying list of all communities sorted by date created.
    """
    page = int(request.args.get("page", 1))
    communities = communities_service.get_communities(page)
    return render_template("communities.html", tab="recent", communities=communities)


@communities_blueprint.route("/communities/top")
def top_communities():
    """
    Route for page displaying list of all communities sorted by most members.
    """
    page = int(request.args.get("page", 1))
    communities = communities_service.get_communities_by_membership(page)
    return render_template("communities.html", tab="top", communities=communities)
