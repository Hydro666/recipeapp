from db import data_layer
from db.sqlite import client

from absl import app
from absl import flags
from absl import logging
import flask

FLAGS = flags.FLAGS

flags.DEFINE_string("sqlite_db_path", None, "DB path for the underlying sqlite db.")
flags.mark_flag_as_required("sqlite_db_path")


def create_flask(test_config=None):
    flask_app = flask.Flask(__name__)

    @flask_app.route("/recipe/<name>")
    def get_recipe(name: str):
        db_connection = client.SQLiteClient(FLAGS.sqlite_db_path)
        logging.info("Trying to get recipe with name: %s", name)
        recipe = db_connection.get_recipe(name)
        if recipe is None:
            flask.abort(404)
        return data_layer.DataSerializer().serialize_structured_recipe_to_json(recipe)
    
    return flask_app



def main(argv):
    create_flask().run()

if __name__ == "__main__":
    app.run(main)