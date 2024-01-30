import unittest

from db import data_layer
from db.sqlite import client

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.SQLiteClient(":memory:")

    def create_and_get_recipe_with_no_ingredients(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=[])
        self.client.create_recipe(recipe)
        actual = self.client.get_recipe(recipe.name)
        self.assertEqual(recipe, actual)

    def create_and_get_recipe_with_ingredients(self):
        pass

if __name__ == "__main__":
    unittest.main()
