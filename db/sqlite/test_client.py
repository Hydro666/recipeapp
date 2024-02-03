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
            recipe_ingredients={
                data_layer.RecipeIngredient("flour", 4),
                data_layer.RecipeIngredient("sugar", 3),
                data_layer.RecipeIngredient("salt", 1),
            },
        )
        self.client.create_recipe(recipe)
        actual = self.client.get_recipe("cake")
        self.assertEqual(recipe, actual)

    def test_create_two_recipes_with_same_name(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)
        with self.assertRaises(client.SQLiteException):
            self.client.create_recipe(recipe)

    def test_get_returns_none_if_no_recipe_inserted_yet(self):
        recipe = data_layer.StructuredRecipe(name="Pascetti", recipe_ingredients=set())
        self.client.create_recipe(recipe)



if __name__ == "__main__":
    unittest.main()
