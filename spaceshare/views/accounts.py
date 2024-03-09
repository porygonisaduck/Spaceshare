"""
Spaceshare accounts view.

URLs include:
"""
import hashlib
import flask
import spaceshare
from spaceshare.views.index import save_file_to_disk


def set_password(password):
    """Use salt and sha512 to get password."""
    algorithm = 'sha512'
    salt = 'a45ffdcc71884853a2cba9e6bc55e812'
    # uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


@spaceshare.app.route('/accounts/login/', methods=['GET'])
def show_login():
    """Display /accounts/login/ route."""
    # print("in login")
    return flask.render_template("login.html")


@spaceshare.app.route('/accounts/', methods=['POST'])
def handle_account():
    """Allow user to manipulate profile."""
    target = '/'
    if flask.request.args.get('target'):
        target = flask.request.args['target']
    connection = insta485.model.get_db()

    if flask.request.form['operation'] == 'login':
        user = flask.request.form['username']
        password = flask.request.form['password']
        handle_account_login(user, password)
        return flask.redirect(target)
    if flask.request.form['operation'] == 'logout':
        return handle_account_logout()
    if flask.request.form['operation'] == 'edit_account':
        return handle_account_edit(target, connection)
    if flask.request.form['operation'] == 'update_password':
        return handle_account_password(target, connection)
    if flask.request.form['operation'] == 'create':
        return handle_account_create(target, connection)
    # Delete
    return handle_account_delete(target, connection)


def handle_account_login(user, password):
    """Allow user to login."""
    if user == '' or password == '':
        flask.abort(400)
    encrypt_pass = set_password(password)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username == ? ",
        (user, )
    )
    check_pass = cur.fetchone()
    if check_pass is None:
        flask.abort(403)
    test_pass = check_pass['password']
    if test_pass != encrypt_pass:
        flask.abort(403)
    # logic for authentification here
    flask.session['username'] = user


@spaceshare.app.route('/accounts/logout/', methods=['POST'])
def handle_account_logout():
    """Allow user to logout."""
    flask.session.clear()
    return flask.redirect('/accounts/login/')


def handle_account_edit(target, connection):
    """Allow user to edit profile."""
    if 'username' not in flask.session:
        flask.abort(403)
    user = flask.session['username']
    if (flask.request.form['fullname'] == '' or
            flask.request.form['email'] == ''):
        flask.abort(400)
    if flask.request.files.get("file"):
        # logic for creating post
        uuid_basename = save_file_to_disk()
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?, filename = ? "
            "WHERE username == ? ",
            (flask.request.form['fullname'],
                flask.request.form['email'], uuid_basename, user, )
        )
    else:
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ? "
            "WHERE username == ? ",
            (flask.request.form['fullname'],
                flask.request.form['email'], user, )
        )
    return flask.redirect(target)


def handle_account_password(target, connection):
    """Allow user to edit password."""
    if 'username' not in flask.session:
        flask.abort(400)
    user = flask.session['username']
    password = flask.request.form['password']
    encrypt_pass = set_password(password)
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username == ? ",
        (user, )
    )
    check_pass = cur.fetchall()[0]['password']
    if check_pass != encrypt_pass:
        flask.abort(403)
    new_pass1 = flask.request.form['new_password1']
    new_pass2 = flask.request.form['new_password2']
    if new_pass1 != new_pass2:
        flask.abort(401)
    new_pass = set_password(new_pass1)
    connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username == ? ",
        (new_pass, user, )
    )
    return flask.redirect(target)


def handle_account_create(target, connection):
    """Allow user to create profile."""
    user = flask.request.form['username']
    password = flask.request.form['password']
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']

    fileobj = flask.request.files["file"]

    uuid_basename = save_file_to_disk()

    if (user == '' or password == '' or
            fullname == '' or email == '' or fileobj == ''):
        flask.abort(400)
    hash_pass = set_password(password)
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username == ? ",
        (user, )
    )
    if cur.fetchone() is not None:
        flask.abort(409)
    connection.execute(
        "INSERT INTO users (username, fullname, email, filename, password)"
        "VALUES (?,?,?,?,?)",
        (user, fullname, email, uuid_basename, hash_pass, )
    )
    flask.session['username'] = user
    return flask.redirect(target)


def handle_account_delete(target, connection):
    """Allow user to delete profile."""
    if 'username' not in flask.session:
        flask.abort(403)
    user = flask.session['username']

    cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner == ? ",
        (user, )
    )
    images = cur.fetchall()

    for image in images:
        filename = image['filename']
        # stem = uuid.uuid4().hex
        # suffix = pathlib.Path(filename).suffix.lower()
        # uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"]/filename
        path.unlink()

    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username == ? ",
        (user, )
    )
    filename2 = cur.fetchone()['filename']
    path = insta485.app.config["UPLOAD_FOLDER"]/filename2
    path.unlink()

    connection.execute(
        "DELETE from users "
        "WHERE username == ? ",
        (user, )
    )
    flask.session.clear()
    return flask.redirect(target)

