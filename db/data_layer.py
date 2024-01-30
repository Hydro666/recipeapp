import abc
import dataclasses
import sqlite3

@dataclasses.dataclass
class StructuredRecipe:
    name: str
    recipe_ingredients: list[tuple[int, str]]


class DataAccessClient:

    @abc.abstractmethod
    def create_recipe(self, recipe: StructuredRecipe):
        ...

    # @abc.abstractmethod
    def get_recipe(self, recipe_name: str) -> StructuredRecipe:
        ...

    # @abc.abstractmethod
    def update_recipe(self, recipe: StructuredRecipe):
        ...

    # @abc.abstractmethod
    def delete_recipe(self, recipe_name: str):
        ...

class SQLiteClient(DataAccessClient):

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

    def create_recipe(self, recipe: StructuredRecipe):
        cur = self._con.cursor()

        cur.execute("INSERT INTO recipe(name) VALUES(?)", (recipe.name,))

    def get_recipe(self, recipe_name: str) -> StructuredRecipe:
        cur = self._con.cursor()

        res = cur.execute("SELECT * FROM recipe WHERE name == ?", (recipe_name,))

        print(res.fetchall())
        return None

if __name__ == '__main__':
    c = SQLiteClient(":memory:")

    recipe = StructuredRecipe('spaghetti', [(3, "tomato"), (4, "wheat")])

    c.create_recipe(recipe)

    r = c.get_recipe(recipe.name)
    print(r)

