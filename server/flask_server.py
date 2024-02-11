from absl import app
from flask import Flask

flask_app = Flask(__name__)

@flask_app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def main(argv):
    flask_app.run()

if __name__ == "__main__":
    app.run(main)