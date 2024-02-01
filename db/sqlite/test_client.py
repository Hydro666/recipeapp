import unittest

from db import data_layer
from db.sqlite import client

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.SQLiteClient(":memory:")

    def test_create_and_get_recipe_with_no_ingredients(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)
        actual = self.client.get_recipe(recipe.name)
        self.assertEqual(recipe, actual)

    def test_create_and_get_recipe_with_ingredients(self):
        recipe = data_layer.StructuredRecipe(
            name="cake",
            recipe_ingredients={(4, "flour"), (3, "sugar"), (1, "salt")},
        )
        self.client.create_recipe(recipe)
        actual = self.client.get_recipe(recipe.name)
        self.assertEqual(recipe, actual)


if __name__ == "__main__":
    unittest.main()
