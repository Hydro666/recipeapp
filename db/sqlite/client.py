import sqlite3

from db import data_layer

class SQLiteException(Exception):
    ...

RECIPE_SCHEMA = """
CREATE TABLE recipe(
    recipe_id INTEGER PRIMARY KEY,
    name UNIQUE
)
"""

INGREDIENT_SCHEMA = """
CREATE TABLE ingredient(
    ingredient_id INTEGER PRIMARY KEY,
    name UNIQUE
)
"""

RECIPE_INGREDIENT_SCHEMA = """
CREATE TABLE recipe_ingredient(
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    ingredient_id INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
)
"""

class SQLiteClient(data_layer.DataAccessClient):

    def __init__(self, db_path: str):
        self._con = sqlite3.connect(db_path)

        self._create_database()

    def _create_database(self):
        cur = self._con.cursor()

        # Create Recipe table
        cur.execute(RECIPE_SCHEMA)

        # Create Ingredient table
        cur.execute(INGREDIENT_SCHEMA)

        # Create recipe ingredient table.
        cur.execute(RECIPE_INGREDIENT_SCHEMA)

    def create_recipe(self, recipe: data_layer.StructuredRecipe):
        """Fails if recipe already inserted"""
        cur = self._con.cursor()

        # Check if recipe already exists.
        res = cur.execute("SELECT * FROM recipe WHERE name == ?", (recipe.name,)).fetchone()
        if res:
            raise SQLiteException(f"Already inserted {recipe}")

        # Insert the recipe.
        cur.execute("INSERT INTO recipe(name) VALUES(?)", (recipe.name,))
        recipe_id = cur.lastrowid

        # Insert the recipe_ingredients.
        for ingredient in recipe.recipe_ingredients:
            cur.execute("INSERT OR IGNORE INTO ingredient(name) VALUES(?)", (ingredient[1],))
            res = cur.execute("SELECT ingredient_id FROM ingredient WHERE name = ?", (ingredient[1],)).fetchone()
            id = res[0]
            cur.execute("INSERT INTO recipe_ingredient(recipe_id, ingredient_id) VALUES(?, ?)", (recipe_id, id))


    def get_recipe(self, recipe_name: str) -> data_layer.StructuredRecipe:
        cur = self._con.cursor()

        res = cur.execute("SELECT tr.name, ti.name FROM recipe AS tr JOIN recipe_ingredient tri USING (recipe_id) JOIN ingredient AS ti USING (ingredient_id) WHERE tr.name == ?", (recipe_name,)).fetchall()
        print(res)
        return data_layer.StructuredRecipe(name=res[1], recipe_ingredients=set())
