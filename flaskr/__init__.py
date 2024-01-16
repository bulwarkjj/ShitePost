"""
telling Python to treat flaskr as a package and create
a app factory instance 
"""
import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # change with random value when done building app
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # importing db.py
    from . import db
    db.init_app(app)

    # importing auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # importing the blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")
    # blog doesn't have a url_prefix since its the main component
    # so we are setting it to the index (root) of the app "/" with teh add_url_rule
    return app