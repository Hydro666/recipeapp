from db import data_layer
from db.sqlite import client

from absl import app
from absl import flags
from flask import Flask

FLAGS = flags.FLAGS

flags.DEFINE_string("sqlite_db_path", None, "DB path for the underlying sqlite db.")

def _convert_structured_recipe_to_json(recipe: data_layer.StructuredRecipe) -> recipe_service_pb2.Recipe:
    out = recipe_service_pb2.Recipe(name=recipe.name)
    for ri in recipe.recipe_ingredients:
        out.recipe_ingredients.add(
            name=ri.name,
            quantity=ri.quantity,
        )
    return out


def create_flask(test_config=None):
    flask_app = Flask(__name__)

    db_connection = client.SQLiteClient(FLAGS.sqlite_db_path)

    @flask_app.route("/recipe/<name>")
    def get_recipe(name: str):
        return "<p>Hello, World!</p>"
    
    return flask_app



def main(argv):
    create_flask().run()

if __name__ == "__main__":
    app.run(main)