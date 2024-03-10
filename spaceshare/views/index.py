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


@spaceshare.app.route('/accounts/phone_number/', methods=['GET'])
def get_phone():
    """Display /accounts/phone_number/ route."""
    return flask.render_template("phone_number.html")

@spaceshare.app.route('/accounts/otp/', methods=['POST'])
def get_otp():
    """Display /accounts/otp/ route."""

    phone_number = flask.request.form['phone-number']

    print(phone_number)
    return flask.render_template("otp.html")


@spaceshare.app.route('/accounts/create/', methods=['GET'])
def create_profile():
    """Display /accounts/create/ route."""
    return flask.render_template("create.html")


def get_user_and_connection():
    """Get the user and connection."""
    user = flask.session['username']

    # Connect to database
    connection = spaceshare.model.get_db()
    return user, connection


def ensure_user_in_database():
    """Ensure the user in the database."""
    user, connection = get_user_and_connection()

    # ENSURE PERSON ACCESSING THIS PAGE IS IN THE DATABASE
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username == ?",
        (user, )
    )
    if len(cur.fetchall()) == 0:  # User is not in database
        flask.abort(404)
    return user, connection


def save_file_to_disk():
    """Save the image file to the disk."""
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    # Compute base name (filename without directory).
    # We use a UUID to avoid
    # clashes with existing files,
    # and ensure that the name is compatible with the
    # filesystem. For best practive,
    # we ensure uniform file extensions (e.g.
    # lowercase).
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = spaceshare.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


def get_user_profile(user, connection):
    """Get the users profile."""
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username == ? ",
        (user, )
    )
    return cur.fetchall()[0]
