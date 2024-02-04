import sqlite3

from db import data_layer


class SQLiteException(Exception): ...


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


def _make_connection(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON")
    return con


class SQLiteClient(data_layer.DataAccessClient):

    def __init__(self, db_path: str):
        self._con = _make_connection(db_path)

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
        with self._con:
            # Check if recipe already exists.
            if (
                self._con.execute(
                    "SELECT * FROM recipe WHERE name == ?", (recipe.name,)
                ).fetchone()
                is not None
            ):
                raise SQLiteException(f"Already inserted {recipe}")

            # Insert the recipe.
            recipe_id = self._con.execute(
                "INSERT INTO recipe(name) VALUES(?)", (recipe.name,)
            ).lastrowid

            # Insert the recipe_ingredients.
            for ingredient in recipe.recipe_ingredients:
                self._con.execute(
                    "INSERT OR IGNORE INTO ingredient(name) VALUES(?)",
                    (ingredient.name,),
                )
                ingredient_id = self._con.execute(
                    "SELECT ingredient_id FROM ingredient WHERE name = ?",
                    (ingredient.name,),
                ).fetchone()[0]
                self._con.execute(
                    "INSERT INTO recipe_ingredient(recipe_id, ingredient_id, quantity) VALUES(?, ?, ?)",
                    (recipe_id, ingredient_id, ingredient.quantity),
                )

    def get_recipe(self, recipe_name: str) -> data_layer.StructuredRecipe | None:
        with self._con:
            # Check if recipe already exists.
            if (
                self._con.execute(
                    "SELECT * FROM recipe WHERE name == ?", (recipe_name,)
                ).fetchone()
                is None
            ):
                return None
            res = self._con.execute(
                "SELECT tr.name, ti.name, tri.quantity FROM recipe AS tr JOIN recipe_ingredient tri USING (recipe_id) JOIN ingredient AS ti USING (ingredient_id) WHERE tr.name == ?",
                (recipe_name,),
            ).fetchall()
        recipe_ingredients = set()
        for row in res:
            recipe_ingredients.add(data_layer.RecipeIngredient(row[1], row[2]))
        return data_layer.StructuredRecipe(
            name=recipe_name, recipe_ingredients=recipe_ingredients
        )

    def update_recipe(self, recipe: data_layer.StructuredRecipe):
        with self._con:
            recipe_row = self._con.execute(
                "SELECT recipe_id FROM recipe WHERE name == ?", (recipe.name,)
            ).fetchone()
            if recipe_row is None:
                raise SQLiteException(f"Recipe {recipe.name} not in table")

            # Remove recipe ingredients from existing ri table.
            self._con.execute(
                "DELETE FROM recipe_ingredient WHERE recipe_id = ?", (recipe_row[0],)
            )

            # Remove the dangling ingredients with no ri entries.
            self._con.execute(
                "DELETE FROM ingredient WHERE ingredient_id NOT IN (SELECT ingredient_id FROM recipe_ingredient)"
            )

            # Insert the ri ingredients.
            for ingredient in recipe.recipe_ingredients:
                self._con.execute(
                    "INSERT OR IGNORE INTO ingredient(name) VALUES(?)",
                    (ingredient.name,),
                )
                ingredient_id = self._con.execute(
                    "SELECT ingredient_id FROM ingredient WHERE name = ?",
                    (ingredient.name,),
                ).fetchone()[0]
                self._con.execute(
                    "INSERT INTO recipe_ingredient(recipe_id, ingredient_id, quantity) VALUES(?, ?, ?)",
                    (recipe_row[0], ingredient_id, ingredient.quantity),
                )
