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
from flask import send_from_directory


@spaceshare.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    # flask.session.clear()

    if 'phone_number' not in flask.session:
        return flask.redirect('/accounts/phone_number/')
    
    # user, connection = get_user_and_connection()

    return flask.render_template("index.html")


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


################### CREATE ACCOUNT ###################

@spaceshare.app.route('/accounts/phone_number/', methods=['GET'])
def get_phone():
    """Display /accounts/phone_number/ route."""
    return flask.render_template("phone_number.html")


@spaceshare.app.route('/accounts/otp/', methods=['POST'])
def get_otp():
    """Display /accounts/otp/ route."""

    phone_number = flask.request.form['phone_number']
    flask.session["phone_number"] = phone_number

    return flask.render_template("otp.html")


@spaceshare.app.route('/accounts/set_password/', methods=['POST'])
def set_password():
    """Display /accounts/set_password/ route."""

    return flask.render_template("set_password.html")


@spaceshare.app.route('/accounts/set_city/', methods=['POST'])
def set_city():
    """Display /accounts/set_city/ route."""

    return flask.render_template("set_city.html")


@spaceshare.app.route('/accounts/account_created/', methods=['POST'])
def account_created():
    """Display /accounts/account_created/ route."""

    return flask.render_template("account_created.html")


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


################### END OF CREATE ACCOUNT ###################


@spaceshare.app.route('/map/', methods=['GET'])
def show_map():
    """Display /map/ route."""
    return flask.render_template("map.html")


@spaceshare.app.route('/profile/', methods=['GET'])
def show_profile():
    """Display /profile/ route."""
    context = {
        "apartment": "apartment.jpg",
        "apartment2": "apartment2.jpg",
        "logo": "logo.png"
    }

    return flask.render_template("profile.html", **context)


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


@spaceshare.app.route('/uploads/<filename>')
def upload_file(filename):
    """Return image file from disk."""
    # unauthenicated user accessing file
    if 'phone_number' not in flask.session:
        flask.abort(403)
    print(spaceshare.app.config['UPLOAD_FOLDER'])
    return flask.send_from_directory(spaceshare.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
