from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World</p>"

if __name__ == "__main__":
    # remember to set debug to false for production
    app.run(host="0.0.0.0", port=5000, debug=True)