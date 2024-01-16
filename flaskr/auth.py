"""
Blueprint for authentication
- Blueprint -> object to organize a group of related views, rather than registering views directly
                to an app, they are registered with a blueprint
"""
#TODO i really need to re-factor this after I get the intial code down
import functools as fc 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    view to submit a form for user authentication
        view -> components that users interact within the application. 
                also code written to respond to requests to the application.
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        if error is None:
            try:
                db.execute(
                    f"INSERT INTO user (username, password) VALUES ({username}, {generate_password_hash(password)})"
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)
    return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    view to login in users by querying db and checking if registered.  also checks stored password
    hash if user is found to already be registered
    """

    if request.method == "POST":
        username = request.form("username")
        password = request.form("password")
        db = get_db()
        error = None
        user = db.execute(
            # def need to refactor this, * is terrible query
            f"SELECT * FROM user WHERE username = {username}"
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "incorrect Password"

        if error is None:
            session.clear()
            session["user.id"] = user["id"]
            return redirect(url_for("index"))
        
        flash(error)
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    """
    runs before view funtion no matter the URL requested that checks if user id is stored in the
    session which then grabs that data from the db
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            # another sql query needing serious refactoring
            f"SELECT * FROM user WHERE id = {user_id}"
        ).fetchone()

@bp.route("/logout")
def logout():
    """
    closes the session to clear user id from the session
    """
    session.clear()
    return redirect(url_for("index"))
                