"""
Spaceshare index (main) view.

URLs include:
/
"""
import pathlib
import uuid
import arrow
import flask
import spaceshare


@spaceshare.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    # flask.session.clear()

    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    user, connection = get_user_and_connection()

    # Query database for posts by the user
    posts = get_user_posts(user, connection)

    # Get posts by people the user is following

    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 == ? ",
        (user, )
    )
    following = cur.fetchall()

    for person in following:
        cur = connection.execute(
            "SELECT * "
            "FROM posts "
            "WHERE owner == ? ",
            (person['username2'], )
        )
        add_posts = cur.fetchall()
        for new_post in add_posts:
            posts.append(new_post)

    # Reorder the posts with highest postid first

    posts.sort(key=post_num, reverse=True)

    # Add all other info posts need
    for post in posts:
        get_post_info(post, user, connection)

    # Add database info to context
    context = {"logname": user, "posts": posts}
    return flask.render_template("index.html", **context)


@spaceshare.app.route('/accounts/edit/', methods=['GET'])
def edit_account():
    """Display /accounts/edit/ route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    user, connection = get_user_and_connection()

    profile = get_user_profile(user, connection)

    # Add database info to context
    context = {"logname": user, "profile": profile}
    return flask.render_template("edit.html", **context)


@spaceshare.app.route('/accounts/password/', methods=['GET'])
def edit_password():
    """Display /accounts/password/ route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    user = flask.session['username']

    # Add database info to context
    context = {"logname": user}
    return flask.render_template("password.html", **context)


@spaceshare.app.route('/accounts/delete/', methods=['GET'])
def delete_profile():
    """Display /accounts/delete/ route."""
    if 'username' not in flask.session:
        return flask.redirect('/accounts/login/')
    user = flask.session['username']

    # Add database info to context
    context = {"logname": user}
    return flask.render_template("delete.html", **context)


@spaceshare.app.route('/accounts/create/', methods=['GET'])
def create_profile():
    """Display /accounts/create/ route."""
    if 'username' in flask.session:
        return flask.redirect('/accounts/edit/')

    return flask.render_template("create.html")


