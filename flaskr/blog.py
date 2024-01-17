from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)
# blueprint -> associates view functions with blueprints when dispatching requests
# and generating URL's between endpoints. groups functionality into reusable components

@bp.route("/")
def index():
    """
    will show all posts, most recent first of the blog
    """
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    
    return render_template("blog/index.html", posts=posts)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """
    user must be logged into to view posts
    if post found, it will display, if not, than it is validated and added
    """
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)"
                f"VALUES ({title}, {body}, {g.user['id']})"
            )
            db.commit()

            return redirect(url_for("blog.index"))
        
    return render_template("blog/create.html")

def get_post(id, check_author=True):
    """
    gets id and author of post and checks if it matches with logged in user
    """
    post = get_db(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p, author_id = u.id"
        f" WHERE p.id = {id}"
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """
    appends a number to the URL to update blog id and use that for URL
    params:
        id -> take <int:id> and prefix URL
    """
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                f"UPDATE post SET title = {title}, body = {body}"
                f" WHERE id = {id}"
            )
            db.commit()
            return redirect(url_for("blog.index"))
        
    return render_template("blog/update.html", post=post)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """
    maps to delete button in update.html
    removes post unquie to the id
    params:
        id -> id -> take <int:id> and prefix URL
    """
    get_post(id)
    db = get_db()
    db.execute(f"DELETE FROM post WHERE id = {id}")
    db.commit()

    return redirect(url_for("blog.index"))