""" Defines the blog blueprint """
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """ Define homepage endpoint 

        The index will show all of the posts, most recent first. 
        A JOIN is used so that the author information from the user 
        table is available in the result.
    """
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET' 'POST'))
@login_required
def create():
    """ Defines the create post view.
    
        Either the form is displayed, or the posted data is validated and 
        the post is added to the database or an error is shown.
        
        A user must be logged in to visit this view, 
        otherwise they will be redirected to the login page.
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_forg('blog.index'))
    return render_template('blog/create.html')