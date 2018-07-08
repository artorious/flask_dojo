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
    if request.method == 'POST':
        # User submitted the login form - validate data
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

