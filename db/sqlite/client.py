import sqlite3

from db import data_layer

class SQLiteException(Exception):
    ...

class SQLiteClient(data_layer.DataAccessClient):

    def __init__(self, db_path: str):
        self._con = sqlite3.connect(db_path)

        self._create_database()

    def _create_database(self):
        # Create Recipe table
        cur = self._con.cursor()

        cur.execute("CREATE TABLE recipe(id INTEGER PRIMARY KEY, name UNIQUE, recipe_ingredient_id)")

        # Create Ingredient table
        cur.execute("CREATE TABLE ingredient(id INTEGER PRIMARY KEY, name UNIQUE)")

        # Create recipe ingredient table.
        cur.execute("CREATE TABLE recipe_ingredient(id INTEGER PRIMARY KEY, recipe_id UNIQUE, ingredient_id UNIQUE, amount, unit)")

    def create_recipe(self, recipe: data_layer.StructuredRecipe):
        """Fails if recipe already inserted"""
        cur = self._con.cursor()

        # Check if recipe already exists.
        res = cur.execute("SELECT * FROM recipe WHERE name == ?", (recipe_name,)).fetchone()
        if res:
            raise SQLiteException(f"Already inserted {recipe}")

        # Insert the ingredients.
        data = [
            (name,) for _, name in recipe.recipe_ingredients
        ]
        cur.executemany("INSERT INTO ingredient(name) VALUES(?)", data)

        # Insert the recipe.
        cur.execute("INSERT INTO recipe(name) VALUES(?)", (recipe.name,))

        # Insert the recipe_ingredients.


    def get_recipe(self, recipe_name: str) -> data_layer.StructuredRecipe:
        cur = self._con.cursor()

        res = cur.execute("SELECT * FROM recipe WHERE name == ?", (recipe_name,)).fetchone()
        return data_layer.StructuredRecipe(name=res[1], recipe_ingredients=[])
