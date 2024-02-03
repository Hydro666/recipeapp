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
    quantity INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
)
"""

class SQLiteClient(data_layer.DataAccessClient):

    def __init__(self, db_path: str):
        self._con = sqlite3.connect(db_path)

        self._create_database()

    def _create_database(self):

        with self._con:
            # Create Recipe table
            self._con.execute(RECIPE_SCHEMA)

            # Create Ingredient table
            self._con.execute(INGREDIENT_SCHEMA)

            # Create recipe ingredient table.
            self._con.execute(RECIPE_INGREDIENT_SCHEMA)

    def create_recipe(self, recipe: data_layer.StructuredRecipe):
        """Fails if recipe already inserted"""
        cur = self._con.cursor()

        with self._con:
            # Check if recipe already exists.
            if self._con.execute("SELECT * FROM recipe WHERE name == ?", (recipe.name,)).fetchone():
                raise SQLiteException(f"Already inserted {recipe}")

            # Insert the recipe.
            recipe_id = self._con.execute("INSERT INTO recipe(name) VALUES(?)", (recipe.name,)).lastrowid

            # Insert the recipe_ingredients.
            for ingredient in recipe.recipe_ingredients:
                self._con.execute("INSERT OR IGNORE INTO ingredient(name) VALUES(?)", (ingredient.name,))
                ingredient_id = cur.execute("SELECT ingredient_id FROM ingredient WHERE name = ?", (ingredient[1],)).fetchone()[0]
                cur.execute("INSERT INTO recipe_ingredient(recipe_id, ingredient_id, quantity) VALUES(?, ?, ?)", (recipe_id, ingredient_id, ingredient.quantity))


    def get_recipe(self, recipe_name: str) -> data_layer.StructuredRecipe:
        with self._con:
            res = self._con.execute("SELECT tr.name, ti.name, tri.quantity FROM recipe AS tr JOIN recipe_ingredient tri USING (recipe_id) JOIN ingredient AS ti USING (ingredient_id) WHERE tr.name == ?", (recipe_name,)).fetchall()
        print(res)
        return data_layer.StructuredRecipe(name=res[1], recipe_ingredients=set())
