""" Blueprint for authentification functions """
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# Associate URL/register with the register view function
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ register view

        When the user visits the /auth/register URL, the register view will
        return HTML with a form for them to fill out. When they submit the
        form, it will validate their input and either show the form again with
        an error message or create the new user and go to the login page
    """
    if request.method == 'POST':
        # User submitted the registration form - validate data
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # validate that username and password are not empty
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            # validate that username is not already registered by querying the
            # database and checking if a result is returned
            # db.execute() takes a SQL query with ? placeholders for any user
            # input, and a tuple of values to replace the place holders with
            # fetchone() returns one row from the query. If the query returned
            # no results, it returns None.
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # If Successful validation, insert new user data into the database
            # while also hashing the password. db.commit to save changes
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            # Redirect to login page
            return redirect(url_for('auth.login'))
        # store error msg for rendering to user
        flash(error)
    # HTML page with registration form
    return render_template('auth/register.html')


# Associate URL/login with the login view function
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ login view

        When the user visits the /auth/login URL, the login view will
        return HTML with a form for them to fill out. When they submit the
        form, it will validate their input and either show the form again with
        an error message or redirect the user to the index/home page
    """
    if request.method == 'POST':
        # User submitted the login form - validate login data for correctness
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # query the user and assign to variable
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            # Non-registered username
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            # Hash submitted password in the same way as the stored hash and
            # securely compare them. a match means valid password
            error = 'Incorrect password.'

        if error is None:
            # Session is a dict that stores data scross requests. When
            # validation succeeds, the user's <id> is stored in a new session.
            # The data is stored on a cookie that is sent to the browser, and
            # the browser then sends it back with subsequent requests. Flask
            # securely signs the data to prevent tampering
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """ Runs before the view function no matter what URL is requested.

        Checks if a <user_id> is stored in the <session> and gets that user's
        data from the database, storing it on <g.user>, which lasts for the
        length of the request.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    """ Removes the user id from the session. """
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """ Require authentification in other views. """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        """ Checks if a user is loaded and redirects to the login page
            otherwise. If a user is loaded the original view is called and
            continues normally.
        """
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

