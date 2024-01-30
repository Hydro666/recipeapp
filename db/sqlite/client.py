import sqlite3

from db import data_layer

class SQLiteClient(data_layer.DataAccessClient):

    def __init__(self, db_path: str):
        self._con = sqlite3.connect(db_path)

        self._create_database()

    def _create_database(self):
        # Create Recipe table
        cur = self._con.cursor()

        cur.execute("CREATE TABLE recipe(id INTEGER PRIMARY KEY, name, recipe_ingredient_id)")

        # Create Ingredient table
        cur.execute("CREATE TABLE ingredient(id INTEGER PRIMARY KEY, name)")

        # Create recipe ingredient table.
        cur.execute("CREATE TABLE recipe_ingredient(id INTEGER PRIMARY KEY, recipe_id, ingredient_id, amount, unit)")

    def create_recipe(self, recipe: data_layer.StructuredRecipe):
        cur = self._con.cursor()

        cur.execute("INSERT INTO recipe(name) VALUES(?)", (recipe.name,))

    def get_recipe(self, recipe_name: str) -> data_layer.StructuredRecipe:
        cur = self._con.cursor()

        res = cur.execute("SELECT * FROM recipe WHERE name == ?", (recipe_name,)).fetchone()
        return data_layer.StructuredRecipe(name=res[0], recipe_ingredients=[])
