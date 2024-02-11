from absl import base_app
from flask import Flask

app == Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def main(argv):
    app.run()

if __name__ == "__main__":
    base_app.run(main)