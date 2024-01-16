"""
Blueprint for authentication
- Blueprint -> object to organize a group of related views, rather than registering views directly
                to an app, they are registered with a blueprint
"""
import functools as fc 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")