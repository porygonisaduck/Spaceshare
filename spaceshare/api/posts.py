"""REST API for posts."""
import flask
import spaceshare
from spaceshare import views


######################################
# FUNCTIONS ##########################

def must_be_loggedin_api(func):
    """Check that there is a user logged in."""
    def checking(*args, **kwargs):
        """Check that user is logged in."""
        # No credentials
        if 'username' not in flask.session:
            if flask.request.authorization is None:
                flask.abort(403)
            else:
                username = flask.request.authorization['username']
                in_password = flask.request.authorization['password']
                views.accounts.handle_account_login(username, in_password)

        return func(*args, **kwargs)
    # this is a fix for overwriting existing endpoint
    checking.__name__ = func.__name__
    return checking


def error_num(num):
    """Create error json and update response code."""
    error = {"message": "Bad Request", "status_code": num}
    return flask.jsonify(error), num


##########################################
# REST API ###############################


